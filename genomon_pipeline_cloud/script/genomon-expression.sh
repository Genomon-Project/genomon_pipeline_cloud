#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace


genomon_expression ${INPUT_DIR}/${SAMPLE}.Aligned.sortedByCoord.out.bam ${OUTPUT_DIR}/${SAMPLE} ${OPTION}

