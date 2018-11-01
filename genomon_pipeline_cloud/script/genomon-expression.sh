#!/bin/bash

set -o errexit
set -o nounset

mkdir -p ${OUTPUT_DIR}
genomon_expression ${INPUT_DIR}/${INPUT_BAM} ${OUTPUT_DIR}/${SAMPLE} ${OPTION}

cp ${OUTPUT_DIR}/${SAMPLE}.sym2fpkm.txt ${OUTPUT_DIR}/${SAMPLE}.genomonExpression.result.txt

