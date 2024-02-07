############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################
set -e

# Prepare the directories
iterbuild=$1
cd ${iterbuild}

# Compile
if [ ! -e build ]; then
    meson setup build
fi
ninja -C build
