#!/bin/bash

set -o errexit
set -o nounset

mkdir -p ${OUTPUT_DIR}
genomon_expression ${INPUT_DIR}/${SAMPLE}.Aligned.sortedByCoord.out.bam ${OUTPUT_DIR}/${SAMPLE} ${OPTION}

cp ${OUTPUT_DIR}/${SAMPLE}.sym2fpkm.txt ${OUTPUT_DIR}/${SAMPLE}.genomonExpression.result.txt

