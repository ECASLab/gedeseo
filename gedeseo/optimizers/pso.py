############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

from numpy import array

from gedeseo.metric import Metric
from gedeseo.optimizer import Optimizer

class Optimizer(Optimizer):
    def ComputeCost(self, points, metrics):
        return {}

    def Optimize(self):
        return {"cost": 0.0, "points": []}
