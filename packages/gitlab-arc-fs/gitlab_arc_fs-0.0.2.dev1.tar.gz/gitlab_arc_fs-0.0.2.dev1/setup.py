from setuptools import setup
setup(
    name='gitlab_arc_fs',  # Name in PyPi
    author="Julian Weidhase",
    author_email="julian.weidhase@rz.uni-freiburg.de",
    description="An experimental and readonly gitlab filesystem extension "
                "for PyFilesystem2.!",
    install_requires=[
        "fs~=2.4.16",
        "urllib3~=1.26.9",
        "requests~=2.28.0",
        "aiohttp"
    ],
    entry_points={
        'fs.opener': [
            'gitlab = gitlab_fs.opener:GitlabFSOpener',
        ]
    },
    license="MY LICENSE",
    packages=['gitlab_arc_fs'],
    version="0.0.2.dev1",
    url="https://git.bwcloud.uni-freiburg.de/julian.weidhase/GitlabFS",
    python_requires='>3.10'
)
