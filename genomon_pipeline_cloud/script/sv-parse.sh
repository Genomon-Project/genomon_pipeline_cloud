#!/bin/bash

set -o errexit
set -o nounset

mkdir -p ${OUTPUT_DIR}

GenomonSV \
    parse \
    ${INPUT_DIR}/${SAMPLE}.markdup.bam \
    ${OUTPUT_DIR}/${SAMPLE} \
    ${OPTION}

