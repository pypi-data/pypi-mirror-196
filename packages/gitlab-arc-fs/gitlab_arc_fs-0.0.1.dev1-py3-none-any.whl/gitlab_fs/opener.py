"""Defines the GitlabFS opener."""

__all__ = ['GitlabFSOpener']

import urllib

import fs # NOQA

from fs.opener import Opener
from fs.opener.errors import OpenerError # NOQA
from fs.base import FS

from gitlab_fs import gitlab_fs  # NOQA


class GitlabFSOpener(Opener):
    """
    The Gitlab FSOpener class represents a gitlab fsopener.
    TODO: Implement error handling.
    """
    protocols = ['gitlab']

    def open_fs(self, fs_url, parse_result, writeable=False,
                create=True, cwd=None) -> FS:
        private_token = parse_result.username
        print(parse_result)

        url = urllib.parse.urlparse(parse_result.resource)

        serverURL = url.scheme + '://' + url.netloc
        namespace = url.path

        print(serverURL, namespace)

        if "ref" in parse_result.params:
            ref = parse_result.params['ref']
            return gitlab_fs.GitlabFS(private_token, serverURL, namespace, ref)

        return gitlab_fs.GitlabFS(private_token, serverURL, namespace)
