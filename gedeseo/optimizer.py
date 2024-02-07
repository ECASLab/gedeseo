############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

from abc import ABC, abstractmethod
from numpy import array

from gedeseo.metric import Metric

class Optimizer(ABC):
    @abstractmethod
    def optimize(self, **kwargs):
        pass
