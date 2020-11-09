#!/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys
# note: this enables to import from src/
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))), "src"))
try:
    import adsa  # noqa:
except ImportError as e:
    print(f"Could not import adsa. Error trace: \"{e}\".")
    sys.exit(1)

# %%

R0s = np.linspace(1.0e-3, 10e-3, 10)
lambda_c = adsa.units.capillary_length()

solutions = []
for R0 in R0s:
    solutions.append(adsa.solver.simulate_droplet_shape(R0))

# %%
cols = int(np.floor(np.sqrt(len(solutions))))
rows = int(np.ceil(len(solutions)/cols))

fig = plt.figure(figsize=(3*cols, 1.5*rows))

for i, solution in enumerate(solutions):
    ax = fig.add_subplot(cols, rows, i+1)

    phi = solution.t
    (X, Z) = solution.y

    x = R0s[i] * X
    z = R0s[i] * Z

    x = np.hstack((-x[::-1], x[1:]))
    z = np.hstack((-z[::-1], -z[1:]))

    ax.plot(x, z, color='k', ls='-', alpha=0.50)

    ax.axis('equal')
    ax.set_title(f"R0 = {R0s[i]*1000.0} mm")

plt.tight_layout()
plt.show()
