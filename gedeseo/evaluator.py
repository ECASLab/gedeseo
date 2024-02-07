############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

from abc import ABC, abstractmethod
from numpy import array

class Evaluator(ABC):
    @abstractmethod
    def evaluate(self):
        pass
