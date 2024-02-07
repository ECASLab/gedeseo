############################################################
# Copyright 2024
# Author: Luis G. Leon-Vega <luis.leon@ieee.org>
############################################################

# Prepare the directories
# $1: cpu id, $2: builddir path, $3: sourcedir
builddir=$2
iterbuild="${builddir}/build-$1"
sourcedir=$3
if [ ! -e ${iterbuild} ]; then
    mkdir -p ${iterbuild}
    cp -ra ${sourcedir}/* ${iterbuild}
fi
# Copy sources
echo -n $iterbuild
