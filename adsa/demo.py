# -*- coding: utf-8 -*-
"""A simulation and visualization demonstration.

This module runs a simple demonstration of the capabilities of the adsa
simulations and analysis.
"""
import logging

from .solver import simulate_droplet_shape
from .analysis import calculate_volume
from .visualisation import plot_drop, plot_drop_3d


def run_demo(args):
    logging.info("Running demonstration.")
    logging.info(f"args={args}")

    R0 = args.R0
    ca = args.ca
    logging.info(f"R0={R0}, ca={ca}")

    y = simulate_droplet_shape(R0, ca)
    logging.debug(f"y.y={y.y}, y.y.shape={y.y.shape}")
    x = y.y[0]
    z = y.y[1]
    vol = calculate_volume(x, z)
    logging.info(f"Droplet volume: {vol}.")
    if args.type == '3d':
        plot_drop_3d(x, z, style=args.style)
    elif args.type == '2d':
        plot_drop(x, z, ca=ca, style=args.style)
