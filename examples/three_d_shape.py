#!/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import time
# note: this enables to import from src/
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))), "src"))
try:
    import adsa  # noqa:
    import adsa.visualisation
    import adsa.threed
except ImportError as e:
    print(f"Could not import adsa. Error trace: \"{e}\".")
    sys.exit(1)


def main():
    R0s = np.linspace(1.0e-3, 10e-3, 10)
    cas = np.linspace(0, 180, 6)[1:]

    solutions = []
    runtimes = []
    for ca in cas:
        for R0 in R0s:
            start_time = time.time()
            solutions.append(adsa.solver.simulate_droplet_shape(R0, ca))
            end_time = time.time()
            runtimes.append(end_time - start_time)

    print(f"Simulated {len(solutions)} droplet shapes in {sum(runtimes):.3f} s.")
    print(f"Fastest run in {1000*min(runtimes):.1f} ms, slowest in {1000*max(runtimes):.1f} ms.")
    print(f"Mean runtime {1000*np.mean(runtimes):.1f} ms.")

    cols = len(R0s)
    rows = len(cas)

    fig = plt.figure(figsize=(3*cols, 2*rows))

    for i, solution in enumerate(solutions):
        col = int(i % cols)
        row = int((i - col)/cols)

        ax = fig.add_subplot(rows, cols, i + 1, projection='3d')

        # Extracte droplet shape from the solution
        phi = solution.t
        (X, Z) = solution.y

        # Re-attach dimensions to the data
        x = R0s[col] * X
        z = R0s[col] * Z

        adsa.visualisation.plot_drop_3d(x, z, ax=ax, style=2)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
