# -*- coding: utf-8 -*-
"""Solver for axisymmetric water droplets.

The core functions of the solver system are located in this file.
"""
import numba
import scipy as sp
import scipy.integrate
import numpy as np
from .units import Quantity, as_quantity, g, rho_water, rho_air, gamma_water


@numba.jit(nopython=True)
def adams_bashforth_derivative(phi, Y, beta, alpha=0.0, gamma=2.0):
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
    K = X*(1 - alpha*k1) / (k1*X - (1 - alpha*k1)*sinphi) \
        if X != 0 and phi != 0 else 1

    dX_dphi = cosphi * K
    dZ_dphi = sinphi * K

    return np.array([dX_dphi, dZ_dphi])


def simulate_droplet_shape(R0, ca_target=180.0, 
                           g=g, 
                           gamma_water=gamma_water, 
                           rho_water=rho_water,
                           rho_air=rho_air):
    """Simulates droplet shape using Young-Laplace differential equations in the
    axisymmetric case.

    Parameters
    ----------
    R0: scalar (in meters) or Quantity
        Radius of curvature at the top of the droplet.
    ca_target: scalar (degrees) or Quantity
        Targeted contact angle. Used to trigger events in the solver.

    Returns
    -------
    droplet_shape : np.ndarray
        Right side of droplet shape as ndarray.
    """
    if isinstance(R0, Quantity):
        R0 = R0.to('m')
    if isinstance(ca_target, Quantity):
        ca_target = ca_target.to('degrees')
    ca_target = np.deg2rad(ca_target)

    # Constants
    g = g.to('m/s^2')
    # Set up parameters for model
    sigma = gamma_water.to("N/m")   # in N/m
    # Tolman length, 0 = ignore curvature dependence of surface tension
    delta = 0.0   # in meters
    alpha = (delta / R0)   # in m/m --> unitless
    drho = (rho_water - rho_air).to("kg/m^3")   # in kg/m^3
    beta = (drho * g * R0 ** 2 / sigma)   # in m
    gamma = 2/(1+2*alpha)   # in unitless

    solution_right = sp.integrate.solve_ivp(
        adams_bashforth_derivative,
        (0, ca_target), (0, 0),
        args=(beta, alpha, gamma), method='BDF')

    return solution_right
