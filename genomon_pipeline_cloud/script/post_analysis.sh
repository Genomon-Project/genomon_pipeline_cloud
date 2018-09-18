#!/bin/bash

set -o errexit
set -o nounset

genomon_root=`realpath $(dirname ${INPUT1})/../..`
mkdir -p ${OUTPUT_DIR}

genomon_pa ${MODE} \
    ${OUTPUT_DIR} \
    ${genomon_root} \
    ${SAMPLE_SHEET} \
    --config_file ${CONFIG_FILE} \
    ${ADD_OPTION}
