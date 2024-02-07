############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

from gedeseo.evaluator import Evaluator
from gedeseo.metric import Metric
from gedeseo.optimizer import Optimizer
from numpy import array

class Gedeseo:
    """
    GEDESEO class
    
    It is the wrapper that makes all the gears work within the
    project. This class is composed of other classes like
    Evaluator, Metric, and Optimizer. This is also in charge of
    orchestrating the optimization flow amongst the different
    instances: evaluation, measure, optimize...
    """
    def __init__(self):
        self._evaluator = None
        self._metrics = []
        self._optimizer = None
        pass

    def find(self) -> array:
        pass

    def attach_evaluator(self, evaluator: Evaluator):
        self._evaluator = evaluator

    def attach_metrics(self, metrics: list(Metric)):
        self._metrics += metrics

    def attach_optimizer(self, optimizer: Optimizer):
        self._optimizer = optimizer
