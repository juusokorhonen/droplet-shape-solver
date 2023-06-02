# -*- coding: utf-8 -*-
"""Three-dimensional analysis tools for droplet shapes.

The functions here can be used to construct three-dimensional versions of the
droplet simulation results.
"""
import numpy as np


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

    xs = np.array([r * np.cos(theta) for r in rho])
    ys = np.array([r * np.sin(theta) for r in rho])
    zs = np.array([z_ * np.ones_like(theta) for z_ in z])

    return xs, ys, zs
