from os.path import abspath, dirname
from typing import Union

import setuptools


def _read_documentation_from_md() -> Union[str, None]:
    """
    Get documentation from readme.md
    :return:
    """

    return None


def dep_packages():
    packages_list = []
    current_path = dirname(abspath(__file__))
    with open(f"{current_path}/requirements.txt") as req_file:
        packages_list = req_file.readlines()
    return packages_list


postman_packages = setuptools.find_packages(
    where="source",
)
setuptools.setup(
    name="postman-sdk",
    version="0.0.1",
    long_description=_read_documentation_from_md(),
    long_description_content_type="text/markdown",
    package_dir={"": "source/"},
    install_requires=dep_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
