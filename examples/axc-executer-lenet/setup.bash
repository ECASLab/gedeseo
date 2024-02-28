#!/bin/bash
############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

AXC_EXECUTER_DIR=axc-executer
EXAMPLE_DIRNAME=$(dirname "$0")

# Configure the project 
cd ${EXAMPLE_DIRNAME}
git clone https://gitlab.com/ecas-lab-tec/approximate-flexible-acceleration-ml/axc-executer.git ${AXC_EXECUTER_DIR}
cd ${AXC_EXECUTER_DIR}
git submodule update --init --recursive
cd ..

# Prepare the builds folder
mkdir -p builds
rm -r builds/*
echo "Dirname: ${EXAMPLE_DIRNAME}"
echo "AxC-Executer: ${AXC_EXECUTER_DIR}"
echo "builds: builds"
