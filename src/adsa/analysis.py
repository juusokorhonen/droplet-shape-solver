#!/usr/bin/env python3
# -*- coding: utf8
import numba
import scipy as sp
import scipy.integrate
import scipy.optimize
import numpy as np
from .units import (Quantity, as_quantity, as_scalar,
                    g, rho_water, rho_air, gamma_water, pi,
                    eotvos_number, capillary_length)


def calculate_volume(X, Z, R0=None):
    """Calculates the volume associated to the `x`, and `z` coordinates by
    assuming an axisymmetric shape.

    Parameters
    ----------
    X : np.ndarray (possibly dimensionless)
        X coordinates of the droplet.
    Z : np.ndarray (possibly dimensionless)
        Y coordinates of the droplet.
    R0 : float (optional, default: None)
        Radius of curvature of the droplet at the apex. If this value is set,
        then `X` and `Z` are assumed to be dimensionless coordinates
        `X` = x/`R0`, `Z` = z/`R0` and the calculations are modified
        accordingly.

    Returns
    -------
    Calculated volume in the same units as `x` and `z`.
    """
    if R0 is None:
        return np.pi*sp.integrate.trapz(X**2, Z)
    return np.pi*R0**3*sp.integrate.trapz(X**2, Z)


def estimate_volume(beta, R0, *, alpha=0.0):
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
    R0: scalar (in meters)
        Radius of curvature of the droplet at the apex.
    alpha: scalar (dimensionless), optional, default = 0.0
        Dimensionless parameter, which relates the thickness of the interface
        "gamma" to the specific size, which is typically the radius of curvature
        at the top of the droplet. `alpha` = gamma / r. (Note: "gamma" here is not
        the surface tension). Note setting `alpha` = 0, will effectively ignore
        curvature dependence of surface tension.

    Returns
    -------
    V: float
        Droplet volume in the same units as `R0`.

    Note
    ----
    This experimental formula is presented in Rekhviashvili and Sokurov, Turk.
    J. Phys. (2018), 42, 699-705.
    """
    return (4.73 * np.pow(R0, 3) / (np.pow(beta, 0.941) + 1.028)
            * np.exp(-2.513 * np.pow(beta, 0.398) * alpha))


def estimate_radius_of_curvature(beta, volume, *, alpha):
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
    R0: float
        Radius of curvature at the apex estimated from the volume.

    Notes
    -----
    See, estimate_volume() for description of the formula.
    """
    return np.cbrt(volume * (np.pow(beta, 0.941) + 1.028)
                   / (4.73*np.exp(-2.513*np.pow(beta, 0.398)*alpha)))
