#!/usr/bin/env python3
############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

import gedeseo as gd

if __name__ == "__main__":
    evaluator = gd.evaluators.PassThruEvaluator()
    metric = gd.metrics.PassThruMetric()
    print("Hello Here")
