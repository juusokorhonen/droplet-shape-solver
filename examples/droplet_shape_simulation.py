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
cas = np.linspace(0, 180, 6)[1:]
lambda_c = adsa.units.capillary_length()

solutions = []
for ca in cas:
    for R0 in R0s:
        solutions.append(adsa.solver.simulate_droplet_shape(R0, ca))

# %%
#cols = int(np.floor(np.sqrt(len(solutions))))
#rows = int(np.ceil(len(solutions)/cols))
cols = len(R0s)
rows = len(cas)

fig = plt.figure(figsize=(3*cols, 2*rows))

for i, solution in enumerate(solutions):
    col = int(i % cols)
    row = int((i - col)/cols)

    ax = fig.add_subplot(rows, cols, i+1)

    phi = solution.t
    (X, Z) = solution.y

    x = R0s[col] * X
    z = R0s[col] * Z

    x = np.hstack((-x[::-1], x[1:]))
    z = np.hstack((-z[::-1], -z[1:]))

    # Move baseline to zero
    z = z - z.min()
    z_reflection = -z*0.25

    ax.fill(x, z, color='k', alpha=0.8)
    ax.fill(x, z_reflection, color='k', alpha=0.5)
    ax.plot(x, z, color='k', ls='-', alpha=1.0)
    ax.plot(x, z_reflection, color='k', ls='-', alpha=0.5)
    ax.axhline(y=0, color='k', ls='-', alpha=1.0)

    ax.axis('equal')
    ax.set_title(f"R0 = {R0s[col]*1000.0:.1f} mm, ca = {cas[row]:.1f}°")

plt.tight_layout()
plt.show()
