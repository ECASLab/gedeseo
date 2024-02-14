#!/usr/bin/env python3

import os

from dse.template import fill_template
from dse.utils import print_header

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

if __name__ == "__main__":
    print_header()
    filled_template = fill_template(template_name, params)
    print(filled_template)
