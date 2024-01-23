# -*- coding: utf-8 -*-
"""Solver for axisymmetric water droplets.

The core functions of the solver system are located in this file.
"""
from typing import Any, Optional

import numba
import scipy as sp
import numpy as np
import numpy.typing as npt

from adsa.analysis import calculate_volume
from adsa.units import g, rho_water, rho_air, gamma_water


@numba.jit(nopython=True)
def adams_bashforth_derivative(
        phi: float,
        Y: npt.NDArray[Any],
        beta: float,
        alpha: float = 0.0,
        gamma: float = 2.0) -> npt.NDArray[Any]:
    r"""
    Calculates the derivate of the Young-Laplace equation using Adams-Bashforth formalism.
    These equations are solved in the non-dimensional form.

    Parameters
    ----------
    phi: scalar (radians)
        Integration parameter, angle calculated from vertical axis.
        This should be set to [0, ca] when calling the solver function.
    Y: np.ndarray (n, )
        An array of dimensionless vectors `X` (dimensionless) = x/r,
        `Z` (dimensionless) = z/r, where r is the radius of curvature at the top
        of the droplet.
    beta: scalar (dimensionless)
        Dimensionless parameter, which describes the capillary length of the
        droplet. `beta` = drho * g * r^2 / sigma, where drho is the difference of
        densities of the liquid and vapour phases, g is gravitational constant,
        r is the radius of curvature at the top of the droplet, and sigma is the
        surface tension of the liquid. (Note. sigma is more specifically the
        surface tension on a planar surface.)
    alpha: scalar (dimensionless), optional, default = 0.0
        Dimensionless parameter, which relates the thickness of the interface
        "gamma" to the specific size, which is typically the radius of curvature
        at the top of the droplet. `alpha` = gamma / r. (Note: "gamma" here is not
        the surface tension). Note setting `alpha` = 0, will effectively ignore
        curvature dependence of surface tension.
    gamma: scalar (dimensionless), optional, default = 2.0
        Dimensionless parameter, which is calculated from `alpha`. It is the
        correction term to the Young-Laplace equation for highly curved
        surfaces.

        .. math::
            \Delta p = \frac{2\sigma}{r}\left(1-\frac{\delta}{r}+\ldots\right)

        gamma = 2 / (1+2 * `alpha`). Note: when `alpha` = 0 (ie. ignoring
        curvature dependence of surface tension), `gamma` = 2. These values can
        be used as defaults, when `delta` is unknown.

    Returns
    -------
    result : np.ndarray, shape (2, )
        dX/dphi (dimensionless)
        dZ/dphi (dimensionless)

    Notes
    -----
    Original formulation for this form of solving the Young-Laplace
    equation in the axisymmetric case can be found in Chapter 3 of
    "An Attempt to Test the Theories of Capillary Action by Comparing
    the Theoretical and Measured Forms of Drops of Fluid" by Francis
    Bashforth and J. C. Adams, Cambridge University Press 1883.

    Further details can be found from:
    Rekhviashvili and Sokurov, Turk. J. Phys (2018), 42, 699-705.

    Dimensionless values X, Z, and P are defined by:
        Y = [X, Z]
        X = x/r
        Z = z/r

    For ignoring the curvature dependence of surface tension (ie. for anything
    that is on the order of millimeters), you can set `alpha`=0 and `gamma`=2.
    """
    (X, Z) = Y   # non-dimensional coordinates

    k1 = gamma + beta * Z
    sinphi = np.sin(phi)
    cosphi = np.cos(phi)
    K = X * (1 - alpha * k1) / (k1 * X - (1 - alpha * k1) * sinphi) \
        if X != 0 and phi != 0 else 1

    dX_dphi = cosphi * K
    dZ_dphi = sinphi * K

    return np.array([dX_dphi, dZ_dphi])


def simulate_droplet_shape(
        R0: float,
        ca_target: float = 180.0,
        *,
        n_steps: Optional[int] = None,
        dimensionless_result: bool = False,
        g: float = g.to("m/s^2"),
        gamma_liquid: float = gamma_water.to("N/m"),
        rho_liquid: float = rho_water.to("kg/m^3"),
        rho_vapour: float = rho_air.to("kg/m^3")
) -> tuple[npt.NDArray[Any], npt.NDArray[Any], npt.NDArray[Any]]:
    """Simulates droplet shape using Young-Laplace differential equations in the
    axisymmetric case.

    Parameters
    ----------
    R0: scalar (unit: meters)
        Radius of curvature at the top of the droplet.
    ca_target: scalar (unit: degrees)
        Targeted contact angle. Used to trigger events in the solver.
    dimensionless_result
        If True, then returns results in dimensionless format.

    Returns
    -------
    (alphas, xs, zs)
        `alphas` : NDArray of points where the function was evaluated
        `xs` : NDArray of x-coordinates.
        `zs` : NDArray of z-coordinates.
    """
    ca_target = np.deg2rad(ca_target)   # Convert to radians

    # Set up parameters for model
    sigma = gamma_liquid   # in N/m
    # Tolman length, 0 = ignore curvature dependence of surface tension
    delta = 0.0   # in meters
    alpha = (delta / R0)   # in m/m --> unitless
    drho = (rho_liquid - rho_vapour)   # in kg/m^3
    beta = (drho * g * R0 ** 2 / sigma)   # in m
    gamma = 2.0 / (1.0 + 2.0 * alpha)   # in unitless

    t_eval = np.linspace(0, ca_target, n_steps) if n_steps is not None else None

    result = sp.integrate.solve_ivp(
        adams_bashforth_derivative,
        (0, ca_target), (0, 0),
        t_eval=t_eval,
        args=(beta, alpha, gamma), method='BDF')

    return result.t, result.y[0], result.y[1]


def solve_droplet_shape_for_volume(
        vol_target: float,
        ca_target: float = 180.0,
        R0_guess: Optional[float] = None
) -> tuple[npt.NDArray[Any], npt.NDArray[Any], npt.NDArray[Any]]:
    """Simulates droplet shape and optimizes the result for the given `vol_target`.
    Note that the shape cannot be calculated directly, but must be numerically
    searched, resulting in much longer run times than `simulate_droplet_shape`.

    Parameters
    ----------
    vol_target (unit: m^3)
        The target volume.
    ca_target (unit: degrees)
        The targeted contact angle.
    **kwargs
        See documentation for `simulate_droplet_shape`.

    Returns
    -------
    (alphas, xs, zs)
        `alphas` : NDArray of points where the function was evaluated
        `xs` : NDArray of x-coordinates.
        `zs` : NDArray of z-coordinates.
    """
    def residual_fun(x: tuple[float], *args, **kwargs) -> float:
        R0 = x[0]
        (_, X, Z) = simulate_droplet_shape(R0, ca_target, dimensionless_result=True)
        vol = calculate_volume(X, Z, R0=R0)
        return (vol - vol_target) / vol_target

    R0_guess = R0_guess or 1e-3   # Random guess

    result: sp.optimize.OptimizeResult = sp.optimize.least_squares(
        fun=residual_fun,
        x0=(R0_guess, ),
        bounds=(0, np.inf),
        ftol=1e-8,
        xtol=1e-8,
        gtol=1e-8,
        loss='linear'
    )

    R0 = float(result.x[0])
    return simulate_droplet_shape(R0, ca_target)


def solve_droplet_shape_for_height(
        height_target: float,
        ca_target: float = 180.0,
        R0_guess: Optional[float] = None,
) -> tuple[npt.NDArray[Any], npt.NDArray[Any], npt.NDArray[Any]]:
    """Simulates droplet shape and optimizes the result for the given `vol_target`.
    Note that the shape cannot be calculated directly, but must be numerically
    searched, resulting in much longer run times than `simulate_droplet_shape`.

    Parameters
    ----------
    height_target (unit: m)
        The target height.
    ca_target (unit: degrees)
        The targeted contact angle.
    **kwargs
        See documentation for `simulate_droplet_shape`.

    Returns
    -------
    (alphas, xs, zs)
        `alphas` : NDArray of points where the function was evaluated
        `xs` : NDArray of x-coordinates.
        `zs` : NDArray of z-coordinates.
    """
    def residual_fun(x: tuple[float, float], *args, **kwargs) -> float:
        R0 = x[0]
        (_, _, Z) = simulate_droplet_shape(R0, ca_target, dimensionless_result=False)
        height = Z[-1]
        return float((height - height_target) / height_target)

    R0_guess = R0_guess or 1e-3   # Random guess

    result: sp.optimize.OptimizeResult = sp.optimize.least_squares(
        fun=residual_fun,
        x0=(R0_guess, ),
        bounds=(0, np.inf),
        ftol=1e-8,
        xtol=1e-8,
        gtol=1e-8,
        loss='linear'
    )

    R0 = float(result.x[0])
    return simulate_droplet_shape(R0, ca_target)
