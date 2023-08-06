"""Python setup.py for project_name package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="email_cleaning_service",
    version="0.2.1",
    description="email_cleaning_service created by paul_lestrat",
    url="https://github.com/JacksonKnew/email_cleaning_service",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="paul_lestrat",
    packages=find_packages(exclude=[".github"]),
    install_requires=read_requirements("requirements.txt"),
)