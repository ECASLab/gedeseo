#!/usr/bin/env python3
############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

import gedeseo as gd
import numpy as np

# From the documentation
def cost_function(I, **kwargs):
    config = {
        **kwargs["params"],
        "I": I
    }

    evaluator = kwargs.get("evaluator")
    metrics = kwargs.get("metrics")

    rawmetrics = evaluator.evaluate(config)
    resmetrics = [metric.extract(rawmetrics) for metric in metrics]
    metric = resmetrics[0]

    # Single metrics and collapse. Some algos can use the
    # hungarian and weighting.
    c = abs(metric["U"] - metric["v_t"] *
            np.log(abs(metric["I"][:, 0] / metric["I_s"])) -
            metric["R"] * metric["I"][:, 0])
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

    # Attach the cost function
    optimizer.attach_cost_function(cost_function)

    # Add the evaluator and metric
    evaluator = gd.evaluators.PassThruEvaluator()
    metric = gd.metrics.PassThruMetric()

    # Assemble the Gedeseo
    gdseo = gd.Gedeseo()
    gdseo.attach_evaluator(evaluator)
    gdseo.attach_metrics([metric])
    gdseo.attach_optimizer(optimizer)

    # Params for the circuit
    config = {
        "U": 10,
        "R": 100,
        "I_s": 9.4e-12,
        "v_t": 25.85e-3
    }

    # Run
    res = gdseo.find(config)
    print(res)
