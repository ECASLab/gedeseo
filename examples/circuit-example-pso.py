#!/usr/bin/env python3
############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

import gedeseo as gd
import numpy as np

# From the documentation
def cost_function(I):
    U = 10
    R = 100
    I_s = 9.4e-12
    v_t = 25.85e-3
    c = abs(U - v_t * np.log(abs(I[:, 0] / I_s)) - R * I[:, 0])
    return c


if __name__ == "__main__":
    # Configure the optimizer
    n_particles = 10
    dimensions = 1
    n_threads = 1
    iterations = 10
    init_position = np.array([[0.09] for i in range(n_particles)])

    # Set-up hyperparameters
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.3}

    # Create the optimizer
    optimizer = gd.optimizers.ParticleSwarmOptimizer(
        npart=n_particles,
        dimensions=dimensions,
        options=options,
        nproc=n_threads,
        iters=iterations,
        initpos=init_position
    )

    # Attach the cost functio
    optimizer.attach_cost_function(cost_function)

    # Optimize
    res = optimizer.optimize()

    print(res)
