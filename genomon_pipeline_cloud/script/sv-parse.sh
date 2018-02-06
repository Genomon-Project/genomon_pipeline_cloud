#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace


GenomonSV \
    parse \
    ${INPUT_DIR}/${SAMPLE}.markedup.bam \
    ${OUTPUT_DIR}/${SAMPLE} \
    ${OPTION}

