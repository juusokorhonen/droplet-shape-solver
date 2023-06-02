# -*- coding: utf-8 -*-
"""Axisymmetric Droplet Shape Analysis

This module can be used to simulate water droplet shapes (of any size) using
axial symmetry, ie. cylindrical coordinates.
"""
__all__ = [
    "units",
    "solver",
    "visualisation",
    "analysis",
    "threed"
]

from lazy_import import lazy_module, lazy_callable

np = lazy_module('numpy')   # Store in sys.modules
arange = lazy_callable('numpy.arange')
array = lazy_callable('numpy.array')
nb = lazy_module('numba')
sp = lazy_module('scipy')
lazy_module('scipy.integrate')
lazy_module('scipy.optimize')
mpl = lazy_module('matplotlib')
plt = lazy_module('matplotlib.pyplot')

# units = lazy_module('adsa.units', level='base')
# solver = lazy_module('adsa.solver', level='base')
# visualisation = lazy_module('adsa.visualisation', level='base')
# analysis = lazy_module('adsa.analysis', level='base')
# threed = lazy_module('adsa.threed', level='base')

from . import units
from . import solver
from . import visualisation
from . import analysis
from . import threed
