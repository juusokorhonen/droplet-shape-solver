# -*- coding: utf-8 -*-
"""Physical units for simulations.

This file provides some helper functions and ready-prepared values that are
needed in the simulations.
"""
import numpy as np

# Constants
rho_water: float = 0.9970474e3   # kg/m^3
rho_air: float = 1.1839  # kg/m^3
gamma_water: float = 72.8e-3   # N/m
rho: float = 1000.0   # kg/m^3
g: float = 9.81   # m/s^2
pi: float = 3.14159285258


def capillary_length(drho: float = rho_water, g: float = g, gamma: float = gamma_water):
    """Returns the capillary length attributed to a density, gravity,
    and surface tension.

    Parameters
    ----------
    drho
        Density of the denser phase (liquid) when compared to the lighter
        phase (vapour/air).
        Unit: kg/m^3
    g
        Gravity.
        Unit: m/s^2
    gamma
        Surface tension of the heavier liquid.
        Unit: N/m (or J/m^2)

    Returns
    -------
    `lambda_c` : Quantity
        The capillary length of the liquid in units of meters.
        Unit: meters
    """
    return np.sqrt(gamma / (drho * g))


def eotvos_number(L: float, lambda_c: float):
    """Returns the Eötvös/Bond number for the given liquid and gravity.

    Parameters
    ----------
    L
        Characteristic length, ie. the radius of curvature at the top of the droplet.
        Unit: m
    lambda_c
        The capillary length of the liquid in units of meters.
        Unit: m

    Returns
    -------
    `eotvos_number` : Quantity
        The Eötvös number for the given parameters.
    """
    return np.power(L / lambda_c, 2)


# Alias for Eötvös number
bond_number = eotvos_number
