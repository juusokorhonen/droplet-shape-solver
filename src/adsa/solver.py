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


@numba.jit(nopython=True)
def adams_bashforth_derivative(phi, Y, alpha, beta, gamma):
    """
    Calculates the derivate of the Young-Laplace equation using Adams-Bashforth formalism.
    These equations are solved in the non-dimensional form.

    Parameters
    ----------
    phi: scalar (radians)
        integration parameter, angle calculated from vertical axis
    Y: np.ndarray (n, )
        An array of dimensionless vectors X (dimensionless), Z (dimensionless).
    P0: scalar (dimensionless)
        Non-dimensional pressure at the top of the droplet.

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

    Dimensionless values X, Z, and P are defined by:
        X = x/lambda_c
        Z = z/lambda_c
        P0 = 2*lambda_c/R0
    """
    (X, Z) = Y   # non-dimensional coordinates

    # This value is re-used in both following eqs
    #k = X / (X * (Z + P0) - np.sin(phi)) if (phi != 0 or X != 0) else 1/(P0-1)
    k1 = gamma + beta * Z
    sinphi = np.sin(phi)
    cosphi = np.cos(phi)
    K = X*(1 - alpha*k1) / (k1*X - (1 - alpha*k1)*sinphi) \
        if X != 0 and phi != 0 else 1

    dX_dphi = cosphi * K
    dZ_dphi = sinphi * K

    return np.array([dX_dphi, dZ_dphi])


def simulate_droplet_shape(R0, ca_target=180.0):
    """Simulates droplet shape using Young-Laplace differential equations in the
    axisymmetric case.

    Parameters
    ----------
    R0: scalar (m) or Quantity
        Radius of curvature at the top of the droplet.
    ca_target: scalar (degrees) or Quantity
        Targeted contact angle. Used to trigger events in the solver.

    Returns
    -------
    droplet_shape : np.ndarray
        Right side of droplet shape as ndarray.
    """
    R0 = as_quantity(R0, 'm')
    ca_target = as_quantity(ca_target, 'degrees')

    #lambda_c = capillary_length(drho=rho_water, g=g, gamma=gamma_water)
    # Eo = eotvos_number(R0, lambda_c)

    #P0 = 2 * lambda_c.magnitude / R0.magnitude
    ca_target = np.deg2rad(ca_target)

    # Set up parameters for model
    sigma = gamma_water.magnitude
    delta = Quantity(0, 'm')   # Tolman length, 0 = ignore curvature dependence of surface tension
    alpha = (delta / R0).magnitude
    drho = (rho_water - rho_air).magnitude
    beta = (drho * g * R0 ** 2 / sigma).magnitude
    gamma = 2/(1+2*alpha)

    solution_right = sp.integrate.solve_ivp(
        adams_bashforth_derivative,
        (0, ca_target.magnitude), (0, 0),
        args=(alpha, beta, gamma), method='BDF')

    return solution_right
