# -*- coding: utf-8 -*-
"""Visualization tools for water droplets.

This file provides functions for easily creating standard visualizations from
the simulated water droplet shapes.
"""
from typing import Optional

import numpy as np
import numpy.typing as npt
import matplotlib as mpl
import matplotlib.pyplot as plt

from adsa import analysis
from adsa import threed


def plot_drop(
        x: npt.NDArray[np.float64],
        z: npt.NDArray[np.float64],
        *,
        x_axis_unit: str = "m",
        z_axis_unit: str = "m",
        color: str = 'k',
        label: str = None,
        ax: mpl.axes.Axes = None,
        scale: float | None = None,
        style: int = 1,
        show: bool = True):
    """Plots the given drop shape.

    Parameters
    ----------
    x: np.ndarray
        Droplet x coordinates
        Unit: User selectable, see x_axis_unit
    z: np.ndarray
        Droplet y coordinates
        Unit: User selectable, see z_axis_unit
    color: str_like (optional, default: 'k', ie. black)
        Color to use for plotting
    label: str (optional)
        Label to use for the line in plot
    annotate: bool (default: True)
        If True, draw in annotations
    ax: mpl.Axes (optional, default: create a new axes)
        An Axes instance to re-use
    scale: tuple ((xmin, xmax), (ymin, ymax)) or None
        If None, axes are autoscaled.
    marker: str or None
        Marker to use for plots. See marker formatting from matplotlib.plot
    style: int
        The style to use. Current values are:
        1: Line plot with annotations
        2: Pseudo-camera view
    show: bool
        Show the chart after plotting.

    Returns
    -------
    The matplotlib figure instance.
    """
    x = np.hstack((-x[::-1], x[1:]))
    z = np.hstack((-z[::-1], -z[1:]))
    z = z - z.min()

    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)

    if style == 1:
        ax.plot(x, z, ls='-', color=color, mec=color, mfc='w',
                mew=1.0, label=label)
        ax.axhline(0, ls='--', color='k')

        ax.set_xlabel(x_axis_unit)
        ax.set_ylabel(z_axis_unit)

    elif style == 2:
        z_reflection = -z * 0.25
        x_reflection = x + 0.25 * z * np.sign(x)

        ax.fill(x, z, color='k', alpha=0.8)
        ax.fill(x_reflection, z_reflection, color='k', alpha=0.7)
        ax.plot(x, z, color='k', ls='-', alpha=1.0)
        ax.axhline(y=0, color='k', ls='-', alpha=1.0)
    else:
        raise RuntimeError(f"Unknown plot style \"{style}\".")

    if scale is None:
        ax.set_ylim(min(z), 1.1 * max(z))
    else:
        ax.set_xlim(*scale[0])
        ax.set_ylim(*scale[1])

    ax.axis('equal')

    if show:
        plt.show()

    return fig


def plot_drop_3d(x, z, *, ax=None, style=1, show=True):
    """Creates a 3D visulisation of the droplet.

    Parameters
    ----------
    x: np.ndarray
        x-coordinate of the perimeter.
    z: np.ndarray
        z-coordinate of the perimeter.
    ax: mpl.Axes or None
        If not None, then use the existing Axes for plottting.
    style: int
        The style used for plotting. Currently supported values are: 1, 2
    show: bool
        Show the chart after plotting.

    Returns
    -------
    The matplotlib figure instance.
    """
    x, y, z = threed.construct_3d_pointcloud_uvsphere(x, z)
    z = -z
    z = z - z.min()

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    if style == 1:
        ax.view_init(elev=5, azim=0)
        ax.set_frame_on(False)

        x_scale = x.max() - x.min()
        y_scale = y.max() - y.min()
        z_scale = z.max() - z.min()
        ax.set_box_aspect((x_scale, y_scale, z_scale))

        ax.scatter(x, y, z, alpha=0.9, color='#1f78b4', s=1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
    elif style == 2:
        ax.view_init(elev=5, azim=0)
        ax.set_frame_on(False)
        ax.set_box_aspect((1, 1, 1))

        x_scale = x.max() - x.min()
        y_scale = y.max() - y.min()
        z_scale = z.max() - z.min()
        ax.set_box_aspect((x_scale, y_scale, z_scale))

        ax.plot_surface(x, y, z, alpha=0.9, color='#1f78b4')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
    else:
        raise RuntimeError(f"Unknown plot style \"{style}\".")

    if show:
        plt.show()

    return fig
