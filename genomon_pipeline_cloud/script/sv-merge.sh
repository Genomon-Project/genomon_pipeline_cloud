#!/bin/bash

set -o errexit

echo -n > ${OUTPUT_DIR}/${PANEL_NAME}.control_info.txt
for i in `seq 1 $MAX_COUNT`; do
    TMP_INPUT_DIR=$(eval echo \$INPUT_DIR_${i})
    if [ "${TMP_INPUT_DIR-UNDEF}" != "UNDEF" ]; then
        if [ "$TMP_INPUT_DIR" != "" ]; then
            SAMPLE=`echo ${TMP_INPUT_DIR} | awk -F "/" '{ print $NF }'`
            echo "${SAMPLE}\t${TMP_INPUT_DIR}/${SAMPLE}" >> ${OUTPUT_DIR}/${PANEL_NAME}.control_info.txt
        fi
    fi
done


GenomonSV \
    merge \
    ${OUTPUT_DIR}/${PANEL_NAME}.control_info.txt \
    ${OUTPUT_DIR}/${PANEL_NAME}.merged.junction.control.bedpe.gz \
    ${OPTION}

