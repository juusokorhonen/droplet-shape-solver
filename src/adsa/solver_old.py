#!/usr/bin/env python3
# -*- coding: utf8
import scipy as sp
import scipy.integrate
import scipy.optimize
import numpy as np
from .constants import Quantity, to_quantity, g, rho, gamma
# Silence NEP 18 warning
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")


def yl(y, s, b, c=rho*g/gamma):
    """
    Calculates the derivate of the Young-Laplace equation

    Parameters
    ----------
    y: np.ndarray
        a vector (phi, x, z)
    s: (placeholder)
        integration parameter (unused)
    b: float
        1/R0 (curvature at top of drop)
    c: float
        drho g / gamma (capillary constant)

    Returns
    -------
    dx/ds: float
    """
    (phi, x, z) = y

    phi = to_quantity(phi, 'radians')
    x = to_quantity(x, 'm')
    z = to_quantity(z, 'm')
    b = to_quantity(b, '1/m')

    dphi_ds = 2*b + c*z
    # Handle special case of x=0 and phi=0
    if x != 0 or phi != 0:
        dphi_ds -= np.sin(phi)/x

    dx_ds = np.cos(phi)
    dz_ds = np.sin(phi)
    return [dphi_ds, dx_ds, dz_ds]


def calc_volume(y):
    """Calculates drop volume from shape matrix.
    Parameters
    ----------
    y: float

    Returns
    -------
    answer: float
    """
    return sp.integrate.trapz(np.pi*y[:, 1]**2, y[:, 2])


def drop_shape_estimate(R, ca, c=rho*g/gamma, *, ca_in_degrees=False):
    """Returns approximate height, R0 (given), volume, path length, and ca as a tuple.

    Parameters
    ----------
    R: float
        Droplet nominal radius, in mm
    ca: float
        Contact angle, in radians
    c: float
        drho g / gamma (capillary constant)
    ca_in_degrees: bool
        Set to True, if `ca` is provided in degrees instead of radians.

    Returns
    -------
    (h, R, vol, l_c, ca): tuple
    h: float
        Height from spherical cap approximation
    R: float
    vol: float
        Volume from spherical cap approximation
    l_c: float
        Path length from spherical cap approximation
    ca: float
        Original contact angle, in radians (regardless of `ca_in_degrees`)
    """
    if ca_in_degrees:
        ca = np.deg2rad(ca)

    x = np.cos(ca)
    # Spherical cap approximation
    vol = np.pi/3.0*R*(x**3-3*x+2)
    # Height from spherical cap approximation
    h = R*(1-x)
    # Path length from spherical cap approximation
    l_c = R*ca

    return (h, R, vol, l_c, ca)


def drop_shape_estimate_for_volume(vol, ca, c=rho*g/gamma,
                                   *, ca_in_degrees=False):
    """Returns approximate height, R0, volume (given), path length, and ca as a tuple.

    Parameters
    ----------
    vol: float
        Target volume for droplet
    ca: float
        Contact angle, in radians
    c: float
        drho g / gamma (capillary constant)
    ca_in_degrees: bool
        Set to True, if `ca` is provided in degrees instead of radians.

    Returns
    -------
    (h, R, vol, l_c, ca): tuple
    h: float
        Height from spherical cap approximation
    R: float
    vol: float
        Volume from spherical cap approximation
    l_c: float
        Path length from spherical cap approximation
    ca: float
        Original contact angle, in radians (regardless of `ca_in_degrees`)
    """
    if ca_in_degrees:
        ca = np.deg2rad(ca)

    x = np.cos(ca)
    # Spherical cap approximation with static R != R(z)
    R = np.power(3 * vol / (np.pi*(x**3-3*x+2)), 1/3)
    # Height of drop from spherical cap approximation
    h = R*(1-x)
    # Path length from spherical cap approximation
    l_c = R*ca

    return (h, R, vol, l_c, ca)


def drop_shape(R0, ca, s=None, volume=None, *, ca_in_degrees=False):
    """Return the drop shape for given R0 and ca.

    Parameters
    ----------
    R0: float
        Radius of curvature at top of droplet.
    ca: float
        Contact angle, in radians
    s: np.ndarray (optional, default: 0...max(lc_R, lc_vol) with 100 steps)
        Integration space
    volume: float (optional, default: estimate from `R`)
    ca_in_degrees: bool
        Set to True, if `ca` is provided in degrees instead of radians.

    Returns
    -------
    y: np.ndarray
    """
    if ca_in_degrees:
        ca = np.deg2rad(ca)

    # Estimate required integration space with spherical cap approximation
    if s is None:
        (h_R, R0, vol_est, lc_R, ca) = drop_shape_estimate(R0, ca)
        if volume is not None:
            # Calculate another estimate
            (h_vol, R0_est, volume, lc_vol, ca) = drop_shape_estimate_for_volume(volume, ca)
        else:
            lc_vol = lc_R
        s = np.linspace(0, max(lc_R, lc_vol), 100)
    y = sp.integrate.odeint(yl, [0.0, 0.0, 0.0], s, args=(1/R0,))

    # Find stop condition
    found_end = False
    for imax, yval in enumerate(y):
        if yval[0] >= ca:
            found_end = True
            break

    if found_end:
        # Remove excess points
        y = y[:imax]
        # Move points to baseline
        y = y - [0, 0, max(y[:, 2])]
    else:
        # s = np.linspace(0, max(s), 100)
        # return drop_shape(R0, ca, s)
        raise RuntimeError(u"Stop condition not found. Perhaps increase s_max? Maximum theta={}, while expecting {}"
                           .format(np.rad2deg(y[-1][0]), np.rad2deg(ca)))

    return y


def fmin(V, volume):
    """Minimization function for solver.

    Parameters
    ----------
    V: float
    volume: float

    Returns
    -------
    result: float
    """
    return (volume - V)**2/V


def drop_shape_for_volume(volume, ca, *, ca_in_degrees=False):
    """Calculates the drop shape for given volume and ca.

    Parameters
    ----------
    volume: float
        Volume of target droplet
    ca: float
        Contact angle of target droplet, in radians.
    ca_in_degrees: bool
        Set to True, if `ca` is provided in degrees instead of radians.

    Returns
    -------
    y: np.ndarray
        Optimized shape for droplet.
    """
    if ca_in_degrees:
        ca = np.deg2rad(ca)

    # Make a guess for the radius of curvature
    (h, R0, volume, l_c, ca) = drop_shape_estimate_for_volume(volume, ca)

    # Minimize error
    res = sp.optimize.minimize(lambda x: fmin(calc_volume(drop_shape(x, ca, volume=volume)),
                                              volume), R0, method='nelder-mead', options={'xtol': 1e-9})

    # Calculate resulting shape
    R0 = res.x[0]
    y = drop_shape(R0, ca)

    # true_volume = calc_volume(y)
    # print("{:.2f} uL --> {:.2f} uL ({:.2f})".format(1e9*volume, 1e9*true_volume, 1e9*fmin(true_volume, volume)))

    return y
