# -*- coding: utf-8 -*-
"""Axisymmetric Droplet Shape Analysis

This module can be used to simulate water droplet shapes (of any size) using
axial symmetry, ie. cylindrical coordinates.
"""
import lazy_loader as lazy

__version__ = "0.0.0"

subpackages = [
    'threed',
    'analysis',
    'visualisation',
    'solver',
    'units'
]

__getattr__, __dir__, _ = lazy.attach(__name__, subpackages)

__all__ = [
    "units",
    "solver",
    "visualisation",
    "analysis",
    "threed"
]
