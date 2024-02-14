#!/usr/bin/env python3

import os
import psutil

from dse.template import fill_template
from dse.utils import print_header
from dse.launcher import run_process

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
params_config = [2, 3]

dirname = os.path.dirname(os.path.abspath(__file__))
template_name = os.path.join(dirname, "templates", "config.hpp.in")

params = [
    [
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1},
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1}
    ], [
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1},
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1},
        {"BW": 14, "IW": 6, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1}
    ]
]


def params_to_vec(params):
    '''
    Converts the params to a vector
    '''
    vec = []
    for layertype in params:
        for config in layertype:
            vec.append(config["BW"])
            vec.append(config["IW"])
    return vec

def vec_to_params(vec):
    '''
    Converts the vector to params structure
    '''
    global params_config
    params = []
    i = 0
    for layertype in params_config:
        params.append([])
        for layers in range(layertype):
            bw = vec[i]
            iw = vec[i + 1]
            i += 2
            param = {"BW": bw, "IW": iw, "ART": "EXACT,EXACT", "DBA": 1, "DBM": 1},
            params[len(params) - 1].append(param)
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

def cost_function(V, **kwargs):
    # Get the CPU affinity
    builddir = kwargs["builddir"]
    coreid = psutil.Process().cpu_num()
    iterbuild = get_iterbuild(builddir, coreid)


    return 0

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
        run_process(f"bash {create_env_script_name} {i} {builddir} {sourcedir}", all_env)

    filled_template = fill_template(template_name, params)
    #print(filled_template)
