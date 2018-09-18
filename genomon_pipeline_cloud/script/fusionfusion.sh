#!/bin/bash

set -o errexit
set -o xtrace

OUTPUT_PREF=${OUTPUT_DIR}/${SAMPLE}
mkdir -p ${OUTPUT_DIR}

if [ "_${MERGED_COUNT_DIR}" != "_" ]; then
    OPTION="${OPTION} --pooled_control_file ${MERGED_COUNT_DIR}/${PANEL_NAME}.merged.Chimeric.count"
fi
/usr/local/bin/fusionfusion --star ${INPUT} --out ${OUTPUT_DIR} --reference_genome ${REFERENCE} ${OPTION}

mv ${OUTPUT_DIR}/star.fusion.result.txt ${OUTPUT_DIR}/${SAMPLE}.star.fusion.result.txt
mv ${OUTPUT_DIR}/fusion_fusion.result.txt ${OUTPUT_DIR}/${SAMPLE}.genomonFusion.result.txt

/usr/local/bin/fusion_utils filt ${OUTPUT_DIR}/${SAMPLE}.genomonFusion.result.txt ${OUTPUT_DIR}/${SAMPLE}.fusion_fusion.result.filt.txt ${FILT_OPTION}

mv ${OUTPUT_DIR}/${SAMPLE}.fusion_fusion.result.filt.txt ${OUTPUT_DIR}/${SAMPLE}.genomonFusion.result.filt.txt

