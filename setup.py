#!/usr/bin/env python3
############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

"""
GEDESEO Setup Tools file
"""

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

name = 'gedeseo'
version = '0.1.0'
author = 'ECASLab (Efficient Computing Across the Stack Laboratory)'
setup(
    name=name,
    version=version,
    description='Generic Extensible Design Space Exploration Optimizer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ECASLab/gedeseo',
    author=author,
    author_email='luis.leon@ieee.org',
    packages=find_packages(
        exclude=[
            "*.tests",
            "*.tests.*",
            "tests.*",
            "tests"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
    install_requires=[
        "psutil >= 5.9.8",
        "pyswarms >= 1.3.0",
        "scipy >= 1.5.0",
        "numpy >= 1.19.1",
        "filelock >= 3.9.0"
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'doc')}},
    extras_require={
        'build_sphinx': ['sphinx']
    },
)
