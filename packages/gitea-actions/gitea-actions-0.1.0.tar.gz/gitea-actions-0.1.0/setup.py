from distutils.core import setup
from setuptools import find_packages

setup(
    name='gitea-actions',
    description="A Python package to interact with Gitea's API",
    version='0.1.0',
    author='awterman',
    install_requires=['requests'],
    packages=find_packages(),
)