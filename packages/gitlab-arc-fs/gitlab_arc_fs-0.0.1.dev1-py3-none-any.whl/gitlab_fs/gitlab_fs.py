from fs.base import FS
from fs.info import Info
from fs.errors import ResourceNotFound, DirectoryExpected,\
                      ResourceReadOnly, Unsupported,\
                      FileExpected  # NOQA
from pathlib import Path
import asyncio
import aiohttp
import urllib3
import threading
import os # NOQA

import requests


try:
    from .gitlab_filestream import FileStreamHandler
except ImportError:
    from gitlab_filestream import FileStreamHandler


class RunThread(threading.Thread):
    """
    Sligthly changed verion of this answer on
    SO:
    https://stackoverflow.com/a/63072524
    Credits to Mark:
    https://stackoverflow.com/users/2606953/mark
    """
    def __init__(self, func, args):
        self.func = func
        self.args = args
        self.result = None
        super().__init__()

    def run(self):
        self.result = asyncio.run(self.func(*self.args))


class GitlabFS(FS):
    """A readonly PyFileSystem extension for gitlab"""

    def __init__(self,
                 token: str,
                 server_url: str):
        super().__init__()
        self.server_url = server_url
        self.hostname = server_url.replace("https://", "")
        self.token = token

        self.fstream = FileStreamHandler(server_url,
                                         token)

        self.accesed_repositories = set()

        # Get the initial (toplevel) directory structure.
        # This is essentially a list of directories which represent
        # all Arcs a user has access to with a given token.
        # The repository metadatastructures themselves are constructed
        # upon changing in into the directory.
        self.repo_list = self._get_accessable_repositories()

        # Create an dictionary, which will be used
        # to store information about the repositories.
        # {Posixpath(repo_path): dict}
        self.repos_dictionary = {}
        self._build_repo_dict()

        # Create an empty dictionary, which will be used to store information
        # about the dictionaries and files inside a repository.
        # {repo_id: dict[Posixpath(filepath): {"is_dir": bool, "name": str}]}
        # TODO: Also save the date-time for a possible cache update later on.
        self.repo_trees_dict = {}

        # Create a metadata dictionary for all repositories as
        # well as for the root directory ("/").
        # {Path: {"info": Info}
        self.info_dict = {}
        self._build_repository_info()

    def _build_repository_info(self):
        """Build info for all accesible repositories (toplevel)"""
        for (path, details) in self.repos_dictionary.items():
            name = path.parts[-1]
            created = details.get('created_at')

            info = {"basic": {"name": name, "is_dir": True},
                    "details": {"accessed": None,
                                "created": created,
                                "metadata_changed": None,
                                "modified": None,
                                "size": None,
                                "type": 1}}
            self.info_dict.update({path: Info(info)})

    def _build_directory_info(self, path: str):
        """
        Builds the directory info for a given path, which
        is the path of a directory INSIDE of a repository.
        The metadata information will be collected for all
        files in the directory.
        Will set metadata as self.metadata_dict[path].
        If path is the path to a file, will raise DirectoryExpected.

        Args:
            path (str): The path to the directory or file
                        to retrieve information about.

        Returns:
            None

        Raises:
            DirectoryExpected: If the path is not a directory.
        """
        if not self.isdir(path):
            raise DirectoryExpected(path)

        # Check if the info of the non-file information
        # (i.e. the directory tree information) of the
        # with path corresponding repository is already build.
        (id, root_path) = self._get_repo_id_path(path)
        if id not in self.repo_trees_dict:
            self._construct_tree_dict(id, root_path)

        repo_tree = self.repo_trees_dict[id]
        for (pth, raw_info) in repo_tree.items():
            if (str(pth.parent) == path or str(pth) == path)\
                                              and self.isdir(pth):
                name = raw_info.get('name')
                info = {"basic": {"name": name, "is_dir": True},
                        "details": {"accessed": None,
                                    "created": None,
                                    "metadata_changed": None,
                                    "modified": None,
                                    "size": None,
                                    "type": 1}}
                self.info_dict.update({pth: Info(info)})

        # TODO: Add the rest of the info object
        raw_info_dict = self.run_async(self._retrieve_metadata, path)
        for (pth, info_raw) in raw_info_dict.items():
            name = info_raw['name']
            size = int(info_raw["size"])
            info = {"basic": {"name": name, "is_dir": False},
                    "details": {"accessed": None,
                                "created": None,
                                "metadata_changed": None,
                                "modified": None,
                                "size": size,
                                "type": 2}}
            self.info_dict.update({pth: Info(info)})

    async def _retrieve_metadata(self, path: str, semaphore: int = None)\
            -> dict[Path, bool | None]:
        """
        This function asynchronously retrieves the (needed) metadata
        by asynchronously sending HTTP-request to the Gitlab-API.

        NOTE: This function should only be called from within
              _build_repository_tree.

        Args:
            path (str): The path to the repository / directory to retrieve
                        information about.
            semaphore (int): Number to limit concurrency to.

        Returns:
            paths_lfs (dict): Dictionary of the filepaths to all files in the
                              (sub)directory specified by path as keys.
                              And wheter they are lfs files (True) or not
                              (False) as values. If the file was not fount on
                              gitlab, the value is None.

        Raises:
            No internal exception handling.
         """
        if semaphore is None:
            semaphore = 10

        if path != "/":
            path = path.strip("/")
        repo_id, repo_path = self._get_repo_id_path(path)
        semaphore = asyncio.BoundedSemaphore(semaphore)
        paths = self._gather_file_paths(path)
        urls = [self.fstream.construct_url(
            str(path),
            repo_id,
            repo_path)
            for path in paths]

        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(
                self.fstream._get_gitlab_metadata(url,
                                                  path,
                                                  session,
                                                  semaphore))
                     for (url, path) in zip(urls, paths)]
            # asyncio.gather returns a list of return values, maintaining the
            # order (i.e. the return value of the first task inserted in the
            # queue will be the first value in temp, regardless of time of
            # completion)
            temp = await asyncio.gather(*tasks)

        paths_info = {key: value for (key, value) in zip(paths, temp)}

        return paths_info

    def _gather_file_paths(self, path: str) -> list[Path]:
        """
        Gather all the paths to (non dir) files in the directory tree,
        which are in the directories specified by path. If path is
        a path to a file, return [path].

        Args:
            path (str): The path to directory or file to gather the paths from.

        Returns:
            directory_list:             A list of paths to (non dir) files
            (list[pathlib.PosixPath])   which lay under the (sub)directory
                                        specified path.

        Raises:
            No internal exception handling.
        """
        # If we are in the root directory, return only the
        # toplevel ARC-View.
        # This information ist stored in self.repos_dictionary.
        if path == "/":
            path_list = [key for key in self.repos_dictionary
                         if key != path]
            return path_list
        else:
            path = path.strip('/')

        path = Path(path)
        # Get the repository id and path.
        # Build the repository tree, if necessary.
        (id, repo_path) = self._get_repo_id_path(path)
        if id not in self.repo_trees_dict:
            self._construct_tree_dict(id, repo_path)

        # Return path, if path is the path to a file.
        repo_tree = self.repo_trees_dict.get(id)
        if not repo_tree.get(path).get("is_dir"):
            return [path]

        path_list = []
        for path_key in repo_tree:
            parent = path_key.parent
            isdir = repo_tree.get(path_key).get("is_dir")
            if parent == path and not isdir:
                path_list.append(path_key)

        return path_list

    def _get_repo_id_path(self, path: str):
        path = Path(path)
        root_path = path.parts[0]
        try:
            id = self.repos_dictionary.get(Path(root_path)).get("id")
        except (KeyError, AttributeError):
            id = None
            root_path = None
        return (id, root_path)

    def _get_accessable_repositories(self):
        """
        Gets information about the repository which are accessible with
        the given token.

        Args: None

        Returns:
            data (dict):   A list of dictionaries containing information about
                           the reposiories.

        Raises:
            SystemExit: if a bad status Code (HTTPError) or a ambigous Request
                        exception is recieved.

        """
        # Maybe Discard all other information besides id, path and
        # is_repository.
        download_url = f"{self.server_url}/api/v4/projects/"
        try:
            with requests.Session() as session:
                r = session.get(download_url,
                                headers={"PRIVATE-TOKEN": self.token},
                                data={"simple": True,
                                      "pagination": "keyset",
                                      "order_by": "id",
                                      "sort": "asc"})
                r.raise_for_status()
        except requests.HTTPError as e:
            print("Bad status code:", r.status_code)
            print("Exiting program")
            raise SystemExit(e)
        except requests.exceptions.Timeout:
            print("Timout error")
            # TODO: Add some retry functionality here.
        except requests.exceptions.RequestException as e:
            print("Recieved ambiugous request exception")
            raise SystemExit(e)

        data = r.json()
        next_references = True

        while next_references:
            try:
                download_url = r.links["next"]["url"]
            except KeyError:
                next_references = False
                session.close()
                continue
            try:
                with requests.Session() as session:
                    r = session.get(download_url,
                                    headers={"PRIVATE-TOKEN":
                                             self.token})
                    r.raise_for_status()
            except requests.HTTPError as e:
                print("Bad status code:", r.status_code)
                print("Exiting program")
                raise SystemExit(e)
            except requests.exceptions.Timeout:
                print("Timout error")
                # TODO: Add some retry functionality here.
            except requests.exceptions.RequestException as e:
                print("Recieved request exception:")
                raise SystemExit(e)
            data.extend(r.json())

        for dict in data:
            dict["path_without_namespace"] = Path(dict.get("path"))
            dict["path_formated"] = Path(dict.pop("path_with_namespace")
                                         .replace("/", "-"))
            dict.update({"is_repository": True,
                         "is_dir": True})

        # Adding the root directory.
        data.append({"path_formated": Path("/"),
                     "path": Path("/"),
                     "is_repository": False,
                     "is_dir": True})

        return data

    def _build_repo_dict(self):
        """
        Construct the directory dict structure from the self.directory_tree.
        Sets the structure as self.directory_dict.

        Args: None
        Returns: None
        Raises: No internal exception handling.
        """
        for el in self.repo_list:
            key = el.get("path_formated")
            value = el
            self.repos_dictionary.update({key: value})

    def _construct_tree_dict(self, repo_id: int,
                             repo_path: str):
        # TODO: Type annotation
        # TODO: Add datetime
        # TODO: Maybe extract everything with requests to gitlab_filestream
        """
        Builds self.repos_dictionary for a given repository(id).

        Args:
            repo_id (int): ID of the repository fot which the directory tree
                           should be constructed.

            path (str):    Path of the directory for prefixing of the
                           directory paths.

        Returns:
            None

        Raises:
            SystemExit: If a RequestError or HTTPError occured.
        """
        # Get the repotree.
        download_url = (f"{self.server_url}/api/v4/projects/"
                        f"{repo_id}"
                        f"/repository/tree")

        # Set the pagination method to keyset, to retrieve the total number of
        # pages. For more information about pagination, see
        # https://docs.gitlab.com/ee/api/repositories.html and
        # https://docs.gitlab.com/ee/api/index.html#keyset-based-pagination
        # In short: This is necessary because all files in the repository will
        # be needed.
        try:
            r = requests.get(download_url,
                             headers={"PRIVATE-TOKEN": self.token},
                             data={"recursive": True,
                                   "pagination": "keyset",
                                   "order_by": "id",
                                   "sort": "asc",
                                   "per_page": 100})
            r.raise_for_status()
        except requests.HTTPError as e:
            print("Bad status code:", r.status_code)
            print("Exiting program")
            raise SystemExit(e)
        except requests.exceptions.Timeout:
            print("Timout error")
            # TODO: Add some retry functionality here.
        except requests.exceptions.RequestException as e:
            print("Recieved request exception")
            print("Exiting program")
            raise SystemExit(e)

        # This could possibly be done asynchronously, but
        # the Gitlab API suggests using the URLs contained in
        # the headers instead of constructing URLs.
        num_pages = int(r.headers["x-total-pages"])

        # tree is a now list of dictionaries, one for each
        # ressource in a agiven repository with, the keys
        # "id", "name", "type", "path" and "mode".
        tree = r.json()

        # Get the repo tree for all files in the repository.
        # This is done by following the links specified in the
        # response. One for each following page.
        for i in range(num_pages-1):
            download_url = r.links["next"]["url"]
            try:
                r = requests.get(download_url,
                                 headers={"PRIVATE-TOKEN":
                                          self.token})
                r.raise_for_status()
            except requests.HTTPError as e:
                print("Bad status code:", r.status_code)
                print("Exiting program")
                raise SystemExit(e)
            except requests.exceptions.Timeout:
                print("Timout error")
                # TODO: Add some retry functionality here.
            except requests.exceptions.RequestException as e:
                print("Recieved request exception:")
                raise SystemExit(e)
            tree.extend(r.json())

        # tree is a list of dictionaries with the keys
        # "id", "name", "type", "path" and mode.
        # Convert list to a dictionary.
        directory_dict = {}
        for element in tree:
            # Prefixing the path with the repository name/path
            path = Path(repo_path, element.get('path'))
            is_dir = True if element.get('type') == 'tree' else False
            info = {"is_dir": is_dir, "name": element.get('name')}
            directory_dict.update({path: info})

        # Also insert the root directory of the repository.
        name = repo_path
        repo_path = Path(repo_path)
        info = {"is_dir": True, "name": name}
        directory_dict.update({repo_path: info})

        self.repo_trees_dict.update({repo_id: directory_dict})
        self.accesed_repositories.add(repo_id)

    def getinfo(self, path: str, namespaces=None):
        """
        """
        if path != "/":
            path = path.strip("/")

        # Ceck if the given path is a path to a repository.
        # If so, the metadata information is already available
        # in self.info_dict.
        if self.isrepository(path):
            try:
                return self.info_dict[Path(path)]
            except KeyError:
                raise ResourceNotFound

        # Check in the repository corresponding to the path
        # was already accessed.
        (id, repo_path) = self._get_repo_id_path(path)
        if id not in self.accesed_repositories:
            self._construct_tree_dict(id, repo_path)

        # Check if metadata for the given path is available already.
        path = Path(path)
        info = self.info_dict.get(path)
        # If not, retrieve the metadata for all files in the given path.
        # If path is the path to a file, then for all files in the same
        # directory
        if info is None:
            if self.isdir(path):
                self._build_directory_info(str(path))
            else:
                # Maybe check here if the partent path is a repo
                self._build_directory_info(str(path.parent))
        # If the metadata for path is nit in self.info_dict,
        # then the resource was not found.
        try:
            return self.info_dict[path]
        except KeyError:
            raise ResourceNotFound(path)

    def listdir(self, path: str) -> list[str]:
        """
        Get a list of the resource names in a directory.
        This method will return a list of the resources in a directory.

        Arguments:
            path (str):     A path to a directory on the filesystem

        Returns:
            directory_list (list): list of names, relative to path.

        Raises:
            fs.errors.DirectoryExpected: If ``path`` is not a directory.
            fs.errors.ResourceNotFound: If ``path`` does not exist.
        """
        if path != "/":
            path = path.strip("/")

        directory_list = []

        # handling of the top-level directory (the view on different ARCs)
        if path == "/":
            directory_list = [str(repo.get("path_formated"))
                              for repo in self.repo_list
                              if repo.get("id") is not None]
            return directory_list

        # Get the root directory of the given path (which will be an
        # repository). Get the repository id. With this, check if the
        # given path is already in self.repos_dictionary.
        # If not, try to build it.
        is_repository = self.isrepository(path)
        (id, root_path) = self._get_repo_id_path(path)

        # If the root path is not in self.repos_dictionary, it can't be
        # a repository which the user has acces to.
        if id is None:
            raise ResourceNotFound
        # Check if the repository described by root path was already build.
        if id not in self.repo_trees_dict:
            self._construct_tree_dict(id, root_path)

        # Check if the path is a valid directory or repository
        # TODO: Revisit this after getinfo and isdir are implemented.
        if (self.repo_trees_dict.get(id).get(Path(path)) is None and
           is_repository is False):
            raise ResourceNotFound(path)
        # Check if the path is a directory.
        if not is_repository:
            if not self.isdir(str(path)):
                raise DirectoryExpected(path)

        paths_list = [path for path in self.repo_trees_dict.get(id)]
        directory_list = [pth.name for pth in paths_list
                          if pth.parent == Path(path)]

        return directory_list

    def isrepository(self, path: str) -> bool:
        """
        """
        if path != "/":
            path = path.strip('/')
        root_path = Path(path).parts[0]
        is_repository = False
        if root_path == path:
            is_repository = True
        return is_repository

    def isdir(self, path: str) -> bool:
        """
        Check if a path maps to an existing directory.

        Arguments:
            path (str): A path on the filesystem.

        Returns:
            bool: `True` if ``path`` maps to a directory.

        """
        path = Path(path)
        # Check if the path is a repository (and therefore a directory).
        if path in self.repos_dictionary:
            return True
        # Check if the repository corresponding to the given path is
        # already build.
        (id, root_path) = self._get_repo_id_path(str(path))
        # If the root path is not in self.repos_dictionary, it can't be
        # a repository which the user has access to. So in this case,
        # the resource is not a found and therefore not a dictionary.
        if id is None:
            return False

        if id not in self.repo_trees_dict:
            self._construct_tree_dict(id, root_path)

        repo_tree = self.repo_trees_dict.get(id)
        if path not in repo_tree:
            return False

        if repo_tree.get(path).get("is_dir"):
            return True

        return False

    def openbin(self, path, mode='r', buffering=-1, **options)\
            -> urllib3.response.HTTPResponse:
        """
        Returns a file like object that can be opened.
        Args:
            path (str): The path to open.
            mode (str): The mode to open the file with. Only read is supported.
            buffering: -
        Returns:
            fp (tempfile.TemporaryFile): A temporary, seekable file object.
            or
            resp (resp.Response): A Response object for a filestream.
        Raises: No internal exception handling.
        NOTE: Only supports read mode ('r')
        TODO: Possibly implement buffering
        TODO: Improve error handling. Maybe get inspired from one of the
              built-in filesystems.
              See https://github.com/PyFilesystem/fs.dropboxfs
        """
        with self._lock:
            if path != "/":
                path = path.strip("/")
            if self.isdir(path):
                raise FileExpected
            if mode != 'r':
                print("Only read operations are supported!")
                raise Unsupported

        (repo_id, repo_path) = self._get_repo_id_path(path)

        r = self.fstream.get_file_stream(path, repo_id, repo_path)

        return r.raw

    def run_async(self, func, *args):
        """
        Sligthly changed verion of this answer on
        SO:
        https://stackoverflow.com/a/63072524
        Credits to Mark:
        https://stackoverflow.com/users/2606953/mark
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            thread = RunThread(func, args)
            thread.start()
            thread.join()
            return thread.result
        else:
            return asyncio.run(func(*args))

    def makedir():
        pass

    def remove():
        pass

    def removedir():
        pass

    def setinfo():
        pass
