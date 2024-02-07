############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

from numpy import array

from gedeseo.metric import Metric

class PassThruMetric(Metric):
    def extract(self, evalres):
        return evalres
