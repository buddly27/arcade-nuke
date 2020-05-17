# :coding: utf-8

import re
import os

from setuptools import setup, find_packages


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCE_PATH = os.path.join(ROOT_PATH, "resource")
SOURCE_PATH = os.path.join(ROOT_PATH, "source")
README_PATH = os.path.join(ROOT_PATH, "README.md")

PACKAGE_NAME = "arcade_nuke"


# Read version from source.
with open(
    os.path.join(SOURCE_PATH, PACKAGE_NAME, "_version.py")
) as _version_file:
    VERSION = re.match(
        r".*__version__ = \"(.*?)\"", _version_file.read(), re.DOTALL
    ).group(1)


# Compute dependencies.
TEST_REQUIRES = [
    "pytest-runner >= 2.7, < 3",
    "pytest >= 4, < 5",
    "pytest-mock >= 1.2, < 2",
    "pytest-xdist >= 1.18, < 2",
    "pytest-cov >= 2, < 3"
]

setup(
    name="arcade-nuke",
    version=VERSION,
    description="Play Arcade Games in Foundry Nuke",
    long_description=open(README_PATH).read(),
    url="http://github.com/buddly27/arcade-nuke",
    keywords="",
    author="Jeremy Retailleau",
    packages=find_packages(SOURCE_PATH),
    package_dir={
        "": "source"
    },
    include_package_data=True,
    tests_require=TEST_REQUIRES,
    extras_require={
        "test": TEST_REQUIRES,
    },
    zip_safe=False
)
