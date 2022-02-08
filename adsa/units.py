#!/usr/bin/env python3
# -*- coding: utf8
import numpy as np
import pint


# Unit registry
ureg = pint.UnitRegistry()
Quantity = ureg.Quantity


# Constants
rho_water = Quantity(0.9970474e3, "kg/m^3")
rho_air = Quantity(1.1839, "kg/m^3")
gamma_water = Quantity(72.8e-3, 'N/m')
rho = Quantity(1000.0, 'kg/m^3')
g = Quantity(9.81, 'm/s^2')
pi = np.pi


def as_quantity(x, quantity):
    """Returns `x` as a `quantity`. 

    Parameters
    ----------
    x : scalar or Quantity or np.ndarray or arr_like
        Value to convert into `quantity`.
    quantity : str
        The quantity to which to convert

    Returns
    -------
    `x` with added quantity units
    """
    if isinstance(x, ureg.Quantity):
        return x.to(quantity)
    else:
        return Quantity(x, quantity)


def as_scalar(x):
    """Returns `x` in unitless scalar format.

    Parameters
    ----------
    x : Quantity or Quantity(np.ndarray)
        The value to convert to unitless format

    Returns
    -------
    `result` : value or np.ndarray
        `x` with the units removed. Units are reduced to the basic form.

    Notes
    -----
    If `x` is not of type Quantity, then it is returned as is.
    """
    if not isinstance(x, ureg.Quantity):
        return x
    return x.magnitude


@ureg.wraps('m', ('kg/m^3', 'm/s^2', 'N/m'), strict=False)
def capillary_length(drho=rho_water, g=g, gamma=gamma_water):
    """Returns the capillary length attributed to a density, gravity,
    and surface tension.

    Parameters
    ----------
    drho : scalar (kg/m^3) or Quantity
        Density of the denser phase (liquid) when compared to the lighter
        phase (vapour/air).
    g : scalar (m/s^2) or Quantity
        Gravity.
    gamma : scalar (N/m or J/m^2) or Quantity
        Surface tension of the heavier liquid.

    Returns
    -------
    `lambda_c` : Quantity
        The capillary length of the liquid in units of meters.
    """
    # drho = as_quantity(drho, "kg/m^3")
    # g = as_quantity(g, "m/s^2")
    # gamma = as_quantity(gamma, "N/m")

    return np.sqrt(gamma / (drho * g))


@ureg.wraps('', ('m', 'm'), strict=False)
def eotvos_number(L, lambda_c):
    """Returns the Eötvös/Bond number for the given liquid and gravity.

    Parameters
    ----------
    L : scalar (m) or Quantity
        Characteristic length, ie. the radius of curvature at the top of the droplet.
    lambda_c : scalar (m) or Quantity
        The capillary length of the liquid in units of meters.

    Returns
    -------
    `eotvos_number` : Quantity
        The Eötvös number for the given parameters.
    """
    # L = as_quantity(L, "m")
    # lambda_c = as_quantity(lambda_c, "m")

    return np.power(L/lambda_c, 2)


# Alias for Eötvös number
bond_number = eotvos_number
