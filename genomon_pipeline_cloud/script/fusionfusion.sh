#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace

OUTPUT_PREF=${OUTPUT_DIR}/${SAMPLE}

PARAM="--grc"

# echo "hello" > ${OUTPUT_DIR}/test.txt

# echo ${INPUT}
# echo ${OUTPUT_DIR}
# echo ${REFERENCE}
# echo ${SAMPLE}

/usr/local/bin/fusionfusion --star ${INPUT} --out ${OUTPUT_DIR} --reference_genome ${REFERENCE} ${PARAM}

mv ${OUTPUT_DIR}/star.fusion.result.txt ${OUTPUT_DIR}/${SAMPLE}.star.fusion.result.txt
mv ${OUTPUT_DIR}/fusion_fusion.result.txt ${OUTPUT_DIR}/${SAMPLE}.fusion_fusion.result.txt


