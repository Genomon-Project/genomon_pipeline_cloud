#!/bin/bash

set -o errexit
set -o nounset

GenomonSV \
    parse \
    ${INPUT_DIR}/${SAMPLE}.markdup.bam \
    ${OUTPUT_DIR}/${SAMPLE} \
    ${OPTION}

