# -*- coding: utf-8 -*-
"""Physical units for simulations.

This file provides some helper functions and ready-prepared values that are
needed in the simulations.
"""
from typing import Union
import numpy as np

class Quantity():
    def __init__(self, value: Union[int, float], unit: str = ""):
        self._value = value
        self._unit = unit

    def to(self, unit):
        if self._unit != unit:
            raise NotImplementedError(f"Unit mismatch: {unit} vs. {self._unit}.")
        return self._value

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    def __eq__(self, other):
        if self.unit != other.unit:
            raise NotImplementedError(f"Unit mismatch: {other.unit} vs. {self._unit}.")
        return self.value == other.value

    def __gt__(self, other):
        if self.unit != other.unit:
            raise NotImplementedError(f"Unit mismatch: {other.unit} vs. {self._unit}.")
        return self.value > other.value

    def __add__(self, other):
        if self.unit != other.unit:
            raise NotImplementedError(f"Unit mismatch: {other.unit} vs. {self._unit}.")
        return Quantity(self.value + other.value, self._unit)

    def __sub__(self, other):
        if self.unit != other.unit:
            raise NotImplementedError(f"Unit mismatch: {other.unit} vs. {self._unit}.")
        return Quantity(self.value - other.value, self._unit)

    def __div__(self, other):
        if self.unit != other.unit:
            raise NotImplementedError(f"Unit mismatch: {other.unit} vs. {self._unit}.")
        return Quantity(self.value / other.value, self._unit)

    def __mul__(self, other):
        if self.unit != other.unit:
            raise NotImplementedError(f"Unit mismatch: {other.unit} vs. {self._unit}.")
        return Quantity(self.value * other.value, self._unit)

    magnitude = value


# Constants
rho_water = Quantity(0.9970474e3, "kg/m^3")
rho_air = Quantity(1.1839, "kg/m^3")
gamma_water = Quantity(72.8e-3, 'N/m')
rho = Quantity(1000.0, 'kg/m^3')
g = Quantity(9.81, 'm/s^2')
pi = 3.14159285258


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
    if isinstance(x, Quantity):
        return x.to(quantity)
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
    if not isinstance(x, Quantity):
        return x
    return x.magnitude


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
    if isinstance(drho, Quantity):
        drho = drho.to('kg/m^3')
    if isinstance(g, Quantity):
        g = g.to('m/s^2')
    if isinstance(gamma, Quantity):
        gamma = g.to('N/m')
    return np.sqrt(gamma / (drho * g))


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
    if isinstance(L, Quantity):
        L = L.to('m')
    if isinstance(lambda_c, Quantity):
        lambda_c = lambda_c.to('m')
    return np.power(L/lambda_c, 2)


# Alias for Eötvös number
bond_number = eotvos_number
