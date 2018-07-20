#!/bin/bash

set -o errexit

echo -n > ${OUTPUT_DIR}/${PANEL_NAME}.Chimeric.count.list
for i in `seq 1 $MAX_COUNT`; do
    TMP_INPUT_DIR=$(eval echo \$INPUT_DIR_${i})
    TMP_SAMPLE=$(eval echo \$SAMPLE_${i})
    if [ "$TMP_INPUT_DIR" != "" ]; then
        echo ${TMP_INPUT_DIR}/${TMP_SAMPLE}.Chimeric.count >> ${OUTPUT_DIR}/${PANEL_NAME}.Chimeric.count.list
    fi
done

OUTPUT=${OUTPUT_DIR}/${PANEL_NAME}.merged.Chimeric.count
chimera_utils merge_control ${OPTION} ${OUTPUT_DIR}/${PANEL_NAME}.Chimeric.count.list ${OUTPUT}

