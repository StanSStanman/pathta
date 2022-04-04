#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: 3-clause BSD
import os
from setuptools import setup, find_packages

__version__ = "0.0.0"
NAME = 'pathta'
AUTHOR = "Etienne Combrisson"
MAINTAINER = "Etienne Combrisson"
EMAIL = 'e.combrisson@gmail.com'
KEYWORDS = "file manager research studies"
DESCRIPTION = "File system manager for research studies"
URL = 'https://github.com/EtienneCmb/pathta'
DOWNLOAD_URL = ("https://github.com/EtienneCmb/pathta/archive/v" +
                __version__ + ".tar.gz")
# Data path :
PACKAGE_DATA = {}


def read(fname):
    """Read README and LICENSE."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name=NAME,
    version=__version__,
    packages=find_packages(),
    package_dir={'pathta': 'pathta'},
    package_data=PACKAGE_DATA,
    include_package_data=True,
    description=DESCRIPTION,
    long_description=read('README.rst'),
    platforms='any',
    setup_requires=['numpy'],
    install_requires=requirements,
    extras_require={},
    dependency_links=[],
    author=AUTHOR,
    maintainer=MAINTAINER,
    author_email=EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    license="BSD 3-Clause License",
    keywords=KEYWORDS,
    classifiers=["Development Status :: 5 - Production/Stable",
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Education',
                 'Intended Audience :: Developers',
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8"
                 ])
