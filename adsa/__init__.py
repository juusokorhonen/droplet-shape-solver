# -*- coding: utf-8 -*-
"""Axisymmetric Droplet Shape Analysis

This module can be used to simulate water droplet shapes (of any size) using
axial symmetry, ie. cylindrical coordinates.
"""
from . import units
from . import solver
from . import visualisation
from . import analysis
from . import threed

VERSION = "0.0.1"

__all__ = [
    "units",
    "solver",
    "visualisation",
    "analysis",
    "threed"
]
