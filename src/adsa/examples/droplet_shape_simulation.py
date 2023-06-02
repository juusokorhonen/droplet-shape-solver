#!/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import time
import adsa
import adsa.visualisation


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

    print("Plotting figures...")
    fig = plt.figure(figsize=(3*cols, 2*rows))

    for i, solution in enumerate(solutions):
        col = int(i % cols)
        row = int((i - col)/cols)

        ax = fig.add_subplot(rows, cols, i+1)

        # Extracte droplet shape from the solution
        phi = solution.t   # noqa: F841
        (X, Z) = solution.y

        # Re-attach dimensions to the data
        x = R0s[col] * X
        z = R0s[col] * Z

        adsa.visualisation.plot_drop(
            x, z, cas[row], ax=ax, style=2)

    print("Plots generated, applying layout...")
    plt.tight_layout()
    print("Showing plot.")
    plt.show()


if __name__ == "__main__":
    main()
