#!/usr/bin/env python3

import os
import psutil
import numpy as np
from scipy import interpolate

from dse.template import fill_template
from dse.utils import print_header
from dse.launcher import run_process

from gedeseo.evaluator import Evaluator
from gedeseo.metric import Metric

'''
  Each configuration must have the following control params (optimisable):
    params[0]: convolution layers (2 elements)
      - BW: data width in bits
      - IW: integer width in bits
      - ART: arirthmetic unit. Set to: EXACT,EXACT for simplicity
      - DBA: number of approximate bits for additions. Set to: 1 for simplicity
      - DBA: number of approximate bits for additions. Set to: 1 for simplicity
    params[1]: dense layers (3 elements, including activation)
      - BW: data width in bits
      - IW: integer width in bits
      - ART: arirthmetic unit. Set to: EXACT,EXACT for simplicity
      - DBA: number of approximate bits for additions. Set to: 1 for simplicity
      - DBA: number of approximate bits for additions. Set to: 1 for simplicity
'''
params_config = {"conv": 2, "dense": 3}

dirname = os.path.dirname(os.path.abspath(__file__))
template_name = os.path.join(dirname, "templates", "config.hpp.in")

# TODO: fix the layers. Instead of having arrays, a dictionary
params = {
    "conv": [
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1},
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1}
    ], "dense": [
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1},
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1},
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1}
    ]
}


def params_to_vec(params):
    '''
    Converts the params to a vector
    '''
    vec = []
    for layertype in params:
        for config in params[layertype]:
            vec.append(config["BW"])
            vec.append(config["IW"])
    return vec


def vec_to_params(vec):
    '''
    Converts the vector to params structure
    '''
    global params_config
    params = {}
    i = 0
    for layertype in params_config:
        params[layertype] = []
        for layers in range(params_config[layertype]):
            bw = vec[i]
            iw = vec[i + 1]
            i += 2
            param = {"BW": bw, "IW": iw,
                     "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1},
            params[layertype].append(param)
    return params


setup_script_name = os.path.join(dirname, "setup.bash")


def parse_setup(res):
    '''
    Parses the setup results to get the dirname, the name of the repo
    and the builddir
    '''
    lines = res["stdout"].split('\n')[1:-1]
    dictfiles = {}
    for line in lines:
        kv = line.split(':')
        k = kv[0]
        v = kv[1].replace(' ', '')
        dictfiles[k] = v
    return dictfiles


create_env_script_name = os.path.join(dirname, "create-env.bash")


def get_iterbuild(builddir, cpuid):
    '''
    Gets the respective build based on the cpuid
    '''
    return os.path.join(builddir, f"build-{cpuid}")


class AxCExecuterEvaluator(Evaluator):
    '''
    Evaluates the params vector into the AxC Executer framework

    It fills the template, copies it to the proper location and runs the
    simulation, collecting the key results
    '''

    def __init__(self):
        # TODO: do the following from a file or from pure synthesis
        # Convolution scale:
        self._conv_consumption = {
            "bw": [4, 6, 8, 10, 12, 16],
            "luts": [2673, 3528, 4182, 4963, 2494, 2762],
            "ffs": [1993, 2905, 3186, 3465, 3918, 4719],
            "dsps": [1, 1, 1, 1, 37, 37],
            "brams": [0, 0, 0, 0, 0, 0]
        }
        # Dense scale:
        self._dense_consumption = {
            "bw": [4, 8, 10, 12, 14, 16],
            "luts": [2112, 2443, 2655, 2199, 2247, 2295],
            "ffs": [1614, 2008, 2191, 2472, 2672, 2873],
            "dsps": [1, 1, 1, 9, 9, 9],
            "brams": [0, 0, 0, 0, 0, 0]
        }
        # Interpolation functions
        self._interpolation = {
            "conv": [
                interpolate.interp1d(
                    self._conv_consumption["bw"], self._conv_consumption["luts"]),  # lut
                interpolate.interp1d(
                    self._conv_consumption["bw"], self._conv_consumption["ffs"]),  # ff
                interpolate.interp1d(
                    self._conv_consumption["bw"], self._conv_consumption["dsps"]),  # dsp
                interpolate.interp1d(
                    self._conv_consumption["bw"], self._conv_consumption["brams"])  # bram
            ],
            "dense": [
                interpolate.interp1d(
                    self._dense_consumption["bw"], self._dense_consumption["luts"]),  # lut
                interpolate.interp1d(
                    self._dense_consumption["bw"], self._dense_consumption["ffs"]),  # ff
                interpolate.interp1d(
                    self._dense_consumption["bw"], self._dense_consumption["dsps"]),  # dsp
                interpolate.interp1d(
                    self._dense_consumption["bw"], self._dense_consumption["brams"])  # bram
            ]
        }

    def evaluate(self, vec, iterbuild):
        config = vec_to_params(vec)
        # Compute the resources (as an aggregation)
        resources = np.array([0., 0., 0., 0.])

        for layertype in config:
            for layer in config[layertype]:
                res = np.array([func(layer[0]["BW"])
                               for func in self._interpolation[layertype]])
                resources += res

        res = {
            "config": config,
            "vec": vec,
            "iterbuild": iterbuild,
            "accuracy": 0.95,
            "resources": resources  # lut, ff, dsp, bram
        }
        return res


class CommunicationMetric(Metric):
    '''
    Evaluates how heavy the communication is in terms of a 64-bit bus

    You want to have less communication overhead (bw/bus)
    '''

    def __init__(self, bus=64):
        self._bus = bus

    def extract(self, evalres):
        vec = evalres["vec"]
        bws = [vec[int(2 * i)] for i in range(len(vec) // 2)]
        maxbw = np.array(bws).max()
        return maxbw / 64


class AccuracyMetric(Metric):
    '''
    Evaluates how accurate is the prediction

    You want to minimise the 1 - acc
    '''

    def __init__(self, threshold=0.8):
        self._acceptable_acc = threshold

    def extract(self, evalres):
        acc = evalres["accuracy"]
        if acc < self._acceptable_acc:
            acc = 0

        return 1 - acc


class ResourcesMetric(Metric):
    '''
    Evaluates how consuming is the network in terms of resources according to
    the configuration

    We want to minimise the resources overall
    '''

    def __init__(self, platform_details):
        self._luts = platform_details["luts"]
        self._ffs = platform_details["ffs"]
        self._brams = platform_details["brams"]
        self._dsps = platform_details["dsps"]
        # lut, ff, dsp, bram
        self._resources = np.array(
            [self._luts, self._ffs, self._dsps, self._brams])

    def extract(self, evalres):
        evalres = np.array(evalres["resources"])
        usage = evalres / self._resources
        return usage.max()


def cost_function(V, **kwargs):
    # Get the CPU affinity
    builddir = kwargs["builddir"]
    coreid = psutil.Process().cpu_num()
    iterbuild = get_iterbuild(builddir, coreid)

    # Get the Gedeseo instances
    axceval = kwargs["evaluator"]
    commsmetric = kwargs["comm-metric"]
    accmetric = kwargs["acc-metric"]
    resmetric = kwargs["res-metric"]

    weights = kwargs["weights"]

    # Evaluate
    evalres = [axceval.evaluate(v, iterbuild) for v in V]

    # Get metrics
    commres = [(weights["comms"] * commsmetric.extract(r)) for r in evalres]
    accres = [(weights["acc"] * accmetric.extract(r)) for r in evalres]
    resres = [(weights["res"] * resmetric.extract(r)) for r in evalres]

    # Assembly into a single numpy
    bipartite = np.array([commres, accres, resres]).T
    costs = bipartite.sum(axis=1)

    return costs


if __name__ == "__main__":
    print_header()
    all_env = {**os.environ}

    # Get the setup result variables
    res = run_process(f"bash {setup_script_name}", all_env)
    files = parse_setup(res)
    builddir = os.path.join(files["Dirname"], files["builds"])
    sourcedir = os.path.join(files["Dirname"], files["AxC-Executer"])

    # Setup environment
    ncores = os.cpu_count()
    for i in range(ncores):
        run_process(
            f"bash {create_env_script_name} {i} {builddir} {sourcedir}", all_env)

    # FPGA Params - K26C
    platform_details = {
        "luts": 37530,
        "ffs": 18600,
        "brams": 200,
        "dsps": 178
    }

    # Minimum accuracy
    min_acc = 0.75

    # Priorities - all same (the sum must be 1)
    weights = {
        "comms": 0.33,
        "acc": 0.33,
        "res": 0.33
    }

    # Gedeseo params
    axceval = AxCExecuterEvaluator()
    commsmetric = CommunicationMetric()
    accmetric = AccuracyMetric(min_acc)
    resmetric = ResourcesMetric(platform_details)

    args = {
        "builddir": builddir,
        "evaluator": axceval,
        "comm-metric": commsmetric,
        "acc-metric": accmetric,
        "res-metric": resmetric,
        "weights": weights
    }

    # Execute gedeseo
    vals = cost_function([params_to_vec(params)], **args)
    print(vals)

    filled_template = fill_template(template_name, params)
    # print(filled_template)
