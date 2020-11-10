#!/usr/bin/env python3
# -*- coding: utf8
import numba
import scipy as sp
import scipy.integrate
import scipy.optimize
import numpy as np
from .units import (Quantity, as_quantity, as_scalar,
                    g, rho_water, rho_air, gamma_water, pi,
                    eotvos_number, capillary_length, ureg)


def construct_3d_pointcloud_uvsphere(rho, z, *, theta=None):
    """Constructs an axisymmetric droplet pointcloud from perimeter.

    Parameters
    ----------
    rho: np.ndarray
        Perimeter rho-coordinate, ie. the "x-coordinate" in the perimeter case.
    z: np.ndarray
        Perimeter y-coordinate.
    theta: np.ndarray (optional, default: None)
        Coordinates for the rotations

    Returns
    -------
    Three-dimensional shape of droplet.
    """
    if theta is None:
        theta = np.linspace(0, 2*np.pi, 32)  # 32 points around

    x = np.array([r * np.cos(theta) for r in rho])
    y = np.array([r * np.sin(theta) for r in rho])
    z = np.array([z_ * np.ones_like(theta) for z_ in z])

    return x, y, z
