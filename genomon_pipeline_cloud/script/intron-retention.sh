#!/bin/bash

set -o errexit
set -o nounset

mkdir -p ${OUTPUT_DIR}
intron_retention_utils \
    simple_count \
    ${INPUT_DIR}/${SAMPLE}.Aligned.sortedByCoord.out.bam \
    ${OUTPUT_DIR}/${SAMPLE}.genomonIR.result.txt \
    ${OPTION}

