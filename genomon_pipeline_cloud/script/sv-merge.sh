#!/bin/bash

set -o errexit

mkdir -p ${OUTPUT_DIR}

echo -n > ${OUTPUT_DIR}/${PANEL_NAME}.control_info.txt
for i in `seq 1 $MAX_COUNT`; do
    TMP_INPUT_DIR=$(eval echo \$INPUT_DIR_${i})
    TMP_SAMPLE=$(eval echo \$SAMPLE_${i})
    if [ "$TMP_INPUT_DIR" != "" ]; then
        echo "${TMP_SAMPLE}\t${TMP_INPUT_DIR}/${TMP_SAMPLE}" >> ${OUTPUT_DIR}/${PANEL_NAME}.control_info.txt
    fi
done


GenomonSV \
    merge \
    ${OUTPUT_DIR}/${PANEL_NAME}.control_info.txt \
    ${OUTPUT_DIR}/${PANEL_NAME}.merged.junction.control.bedpe.gz \
    ${OPTION}

