############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

import pyswarms as ps
import numpy as np

from gedeseo.metric import Metric
from gedeseo.optimizer import Optimizer


class ParticleSwarmOptimizer(Optimizer):
    def __init__(self, npart, dimensions, options,
                 nproc=1, iters=10, bounds=None,
                 center=1.0, initpos=None, tol=-np.inf):
        self._npart = npart
        self._dimensions = dimensions
        self._options = options
        self._center = center
        self._initpos = initpos
        self._nproc = nproc
        self._iters = iters
        self._tolerance = tol
        self._bounds = bounds

        self._optimizer = ps.single.GlobalBestPSO(
            n_particles=self._npart,
            dimensions=self._dimensions,
            init_pos=self._initpos,
            options=self._options,
            bounds=self._bounds,
            center=self._center,
            ftol=self._tolerance,
        )

        self._compute_cost_function = None

    def attach_cost_function(self, func):
        self._compute_cost_function = func

    def optimize(self):
        if not self._compute_cost_function:
            raise NotImplementedError(
                "Cannot optimize without a cost function")

        cost, pos = self._optimizer.optimize(
            self._compute_cost_function,
            iters=self._iters,
            n_processes=self._nproc,
            verbose=False
        )

        return {"cost": cost, "points": pos, "iters": self._iters}
