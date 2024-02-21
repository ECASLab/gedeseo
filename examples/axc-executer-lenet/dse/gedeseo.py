############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

from gedeseo.evaluator import Evaluator
from gedeseo.metric import Metric

from numpy import array


class PassThruEvaluator(Evaluator):
    def evaluate(self, config):
        return config

class PassThruMetric(Metric):
    def extract(self, evalres):
        return evalres
