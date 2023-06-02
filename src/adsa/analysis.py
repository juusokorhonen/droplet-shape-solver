"""Tools for extracting values from droplet shapes.

This module contains helper functions for calculating physical quantities from
droplet shape profiles provided by the solver functions.
"""
from typing import Optional, Any

import scipy as sp
import numpy as np
import numpy.typing as npt
import math


def calculate_volume(
        X: npt.NDArray[Any],
        Z: npt.NDArray[Any],
        R0: Optional[float] = None) -> float:
    """Calculates the volume associated to the `x`, and `z` coordinates by
    assuming an axisymmetric shape.

    Parameters
    ----------
    X : NDArray (possibly dimensionless)
        X coordinates of the droplet.
    Z : NDArray (possibly dimensionless)
        Y coordinates of the droplet.
    R0 : float (optional, unit: m, default: None)
        Radius of curvature of the droplet at the apex. If this value is set,
        then `X` and `Z` are assumed to be dimensionless coordinates
        `X` = x/`R0`, `Z` = z/`R0` and the calculations are modified
        accordingly.

    Returns
    -------
    Calculated volume in the same units as `x` and `z`, ie "m^3".
    """
    if R0 is None:
        return float(np.pi * sp.integrate.trapz(X**2, Z))
    return float(np.pi * math.pow(R0, 3) * sp.integrate.trapz(X**2, Z))


def estimate_volume(
        beta: float,
        R0: float,
        *,
        alpha: float = 0.0) -> float:
    """Estimate droplet volume from parameters.

    Parameters
    ----------
    beta: scalar (dimensionless)
        Dimensionless parameter, which describes the capillary length of the
        droplet. `beta` = drho * g * r^2 / sigma, where drho is the difference of
        densities of the liquid and vapour phases, g is gravitational constant,
        r is the radius of curvature at the top of the droplet, and sigma is the
        surface tension of the liquid. (Note. sigma is more specifically the
        surface tension on a planar surface.)
    R0: scalar (unit: m)
        Radius of curvature of the droplet at the apex.
    alpha: scalar (dimensionless), optional, default = 0.0
        Dimensionless parameter, which relates the thickness of the interface
        "gamma" to the specific size, which is typically the radius of curvature
        at the top of the droplet. `alpha` = gamma / r. (Note: "gamma" here is not
        the surface tension). Note setting `alpha` = 0, will effectively ignore
        curvature dependence of surface tension.

    Returns
    -------
    V: float (unit: m^3)
        Droplet volume in the same units as `R0`, ie. m^3.

    Note
    ----
    This experimental formula is presented in Rekhviashvili and Sokurov, Turk.
    J. Phys. (2018), 42, 699-705.
    """
    return (4.73 * math.pow(R0, 3) / (math.pow(beta, 0.941) + 1.028)
            * math.exp(-2.513 * math.pow(beta, 0.398) * alpha))


def estimate_radius_of_curvature(
        beta: float,
        volume: float,
        *,
        alpha: float = 0.0) -> float:
    """Estimate radius of curvature from volume.

    Parameters
    ----------
    beta: scalar (dimensionless)
        Dimensionless parameter, which describes the capillary length of the
        droplet. `beta` = drho * g * r^2 / sigma, where drho is the difference of
        densities of the liquid and vapour phases, g is gravitational constant,
        r is the radius of curvature at the top of the droplet, and sigma is the
        surface tension of the liquid. (Note. sigma is more specifically the
        surface tension on a planar surface.)
    volume: scalar (in meters^3)
        Volume of the droplet.
    alpha: scalar (dimensionless), optional, default = 0.0
        Dimensionless parameter, which relates the thickness of the interface
        "gamma" to the specific size, which is typically the radius of curvature
        at the top of the droplet. `alpha` = gamma / r. (Note: "gamma" here is not
        the surface tension). Note setting `alpha` = 0, will effectively ignore
        curvature dependence of surface tension.

    Returns
    -------
    R0: float (unit: m)
        Radius of curvature at the apex estimated from the volume.

    Notes
    -----
    See, estimate_volume() for description of the formula.
    """
    return np.cbrt(volume * (math.pow(beta, 0.941) + 1.028) / (4.73*math.exp(-2.513*math.pow(beta, 0.398)*alpha)))
