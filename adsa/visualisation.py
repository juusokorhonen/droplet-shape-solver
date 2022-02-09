# -*- coding: utf-8 -*-
"""Visualization tools for water droplets.

This file provides functions for easily creating standard visualizations from
the simulated water droplet shapes.
"""
import numpy as np
import matplotlib.pyplot as plt
from . import analysis, threed


def plot_drop(x, z, ca, *, color='k', label=None, ax=None, scale=None, style=1):
    """Plots the given drop shape.

    Parameters
    ----------
    x: np.ndarray
        Droplet x coordinates
    z: np.ndarray
        Droplet y coordinates
    ca: float
        Contact angle of the droplet.
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
    """
    x = np.hstack((-x[::-1], x[1:]))
    z = np.hstack((-z[::-1], -z[1:]))
    z = z - z.min()

    show_after_plot = False
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        show_after_plot = True

    if style == 1:
        ax.plot(x, z, ls='-', color=color, mec=color, mfc='w',
                mew=1.0, label=label)
        ax.axhline(0, ls='--', color='k')

        ax.set_xlabel("mm")
        ax.set_ylabel("mm")

        volume = analysis.calculate_volume(x, z)
        ax.text(0.5, 0.5, u"Contact angle: {:.4}\nVolume: {:.4} uL".format(
                ca, volume*1e9),
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)

    elif style == 2:
        z_reflection = -z * 0.25
        x_reflection = x + 0.25*z*np.sign(x)

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

    if show_after_plot:
        plt.show()


def plot_drop_3d(x, z, *, ax=None, style=1):
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
    """
    x, y, z = threed.construct_3d_pointcloud_uvsphere(x, z)
    z = -z
    z = z - z.min()

    show_after_plot = False
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        show_after_plot = True

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

    if show_after_plot:
        plt.show()
