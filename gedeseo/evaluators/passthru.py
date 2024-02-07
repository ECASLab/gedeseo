############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

from numpy import array

from gedeseo.evaluator import Evaluator

class PassThruEvaluator(Evaluator):
    def evaluate(self, config):
        return config
