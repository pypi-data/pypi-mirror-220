#!/usr/bin/env python

from setuptools import setup,find_packages
import sys

from pathlib import Path
this_directory = Path(__file__).parent
README = (this_directory / "README.md").read_text()

pkgname = "python-eigen-ingenuity"
# Invoke setup
setup(
    name=pkgname,
    version='0.4.16',
    author='Murray Callander',
    author_email='info@eigen.co',
    url='https://www.eigen.co/',
    description="A python library used to query data from the Eigen Ingenuity system",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages("."),
    license='Apache License 2.0',
    install_requires=["pandas",
                    "requests",
                    "urllib3",
                    "msal",
                    "keyring"],
)
