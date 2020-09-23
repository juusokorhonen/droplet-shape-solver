#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Setup script for the droplet-shape-solver module.

@file           setup.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import sys
import setuptools
import pkg_resources
assert sys.version_info.major == 3


def get_version(version_file='VERSION'):
    """Returns the current library version.
    @return str -- Current semantical version.
    """
    return str(pkg_resources.parse_version(open(version_file, 'r').read().strip()))


def get_short_description(readme_file='README.md'):
    """Returns the short description of the package.
    @return str -- short description
    """
    return open(readme_file, 'r').readlines(1000)[2].strip()


def get_long_description(readme_file='README.md'):
    """Returns the long description of the package.
    @return str -- Long description
    """
    return "".join(open(readme_file, 'r').readlines()[2:])


setuptools.setup(
    long_description_content_type="text/markdown",
    version=get_version()
)
