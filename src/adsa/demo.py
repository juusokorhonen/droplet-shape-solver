# -*- coding: utf-8 -*-
"""A simulation and visualization demonstration.

This module runs a simple demonstration of the capabilities of the adsa
simulations and analysis.
"""

import logging
from pathlib import Path
import csv

import matplotlib.pyplot as plt

from adsa.solver import simulate_droplet_shape
from adsa.analysis import calculate_volume
from adsa.visualisation import plot_drop, plot_drop_3d


def run_demo(args):
    logging.info("Running demonstration.")
    logging.info(f"args={args}")

    R0 = args.R0
    ca = args.ca
    logging.info(f"R0={R0}, ca={ca}")

    alphas, xs, zs = simulate_droplet_shape(R0, ca)
    vol = calculate_volume(xs, zs)

    logging.info(f"Droplet volume: {vol}.")
    fig = None
    if args.type == '3d':
        fig = plot_drop_3d(xs, zs, style=args.style, show=(not args.noshow))
    elif args.type == '2d':
        fig = plot_drop(xs, zs, ca=ca, style=args.style, show=(not args.noshow))

    if fig is not None and args.save:
        filepath = Path(args.save)
        if (filepath.exists()):
            logging.error(f"Will not overwrite existing file: {filepath}")
        else:
            logging.info(f"Saving plot output to {filepath}")
            fig.savefig(filepath)


def run_sweep(args):
    logging.info("Running sweep.")
    logging.info(f"args={args}")

    with open(args.results, 'w') as results_file:
        logging.info(f"Opened {results_file} for writing results.")
        writer = csv.DictWriter(results_file, delimiter=',', fieldnames=["R0", "CA", "Volume"])
        writer.writeheader()

        for R0 in args.R0:
            for ca in args.ca:
                alphas, xs, zs = simulate_droplet_shape(R0, ca)
                vol = calculate_volume(xs, zs)

                logging.info(f"CA={ca} deg; R0={R0*1000} mm; Vol={vol*1e6} µL")
                writer.writerow({'R0': R0 * 1000, 'CA': ca, 'Volume': vol * 1e6})

                fig = plot_drop(xs, zs, ca=ca, style=args.style, show=False)
                for ext in args.filetypes:
                    filepath = Path(args.filename.format(ca=ca, R0=1000 * R0, ext=ext))
                    if (filepath.exists()):
                        logging.error(f"Will not overwrite existing file: {filepath}")
                    else:
                        logging.info(f"Saving plot output to {filepath}")
                        fig.savefig(filepath)
                plt.close(fig)
