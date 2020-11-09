#!/usr/bin/env python3
# -*- coding: utf8
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from . import solver


def plot_drop(y, *, color='k', label=None, annotate=True, ax=None, autoscale=True, show_after_plot=True):
    """Plots the given drop shape.
    
    Parameters
    ----------
    y: np.ndarray
        Droplet shape
    color: str_like (optional, default: 'k', ie. black)
        Color to use for plotting
    label: str (optional)
        Label to use for the line in plot
    annotate: bool (default: True)
        If True, draw in annotations
    ax: mpl.Axes (optional, default: create a new axes)
        An Axes instance to re-use
    autoscale: bool (default: True)
        If True, visible area is autoscaled to data
    show_after_plot: bool (default: True)
        If True, plot is shown after calling the function
    """
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
    x_data = list(-y[:, 1][::-1]) + list(y[:, 1])
    y_data = list(-y[:, 2][::-1]) + list(-y[:, 2])
    ax.plot(x_data, y_data, ls='-', marker='o', color=color, mec=color, mfc='w',
            mew=1.0, label=label)
    ax.axhline(0, ls='--', color='k')
    if autoscale:
        ax.set_ylim(min(y_data), 1.1*max(y_data))
    ax.set_aspect('equal')
    ax.set_xlabel("mm")
    ax.set_xticklabels(1000*ax.get_xticks())
    ax.set_ylabel("mm")
    ax.set_yticklabels(1000*ax.get_yticks())
    if annotate:
        volume = solver.calc_volume(y)
        ax.text(0.5, 0.5, u"Contact angle: {:.4}\nVolume: {:.4} uL".format(
                np.rad2deg(y[-1, 0]), volume*1e9),
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)
    if show_after_plot:
        plt.show()
