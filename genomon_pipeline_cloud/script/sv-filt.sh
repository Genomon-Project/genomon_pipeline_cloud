#!/bin/bash

set -o errexit
set -o nounset

TUMOR_BAM=${TUMOR_BAM_DIR}/${TUMOR_BAM}

ARGUMENT="${TUMOR_BAM} ${TUMOR_SV_DIR}/${TUMOR_SAMPLE} ${REFERENCE}"

if [ ! _${CONTROL_PANEL} = "_None" ]
then
    ARGUMENT="${ARGUMENT} --non_matched_control_junction ${MERGED_JUNCTION}/${CONTROL_PANEL}.merged.junction.control.bedpe.gz"
fi

if [ ! _${NORMAL_SAMPLE} = "_None" ]
then
    NORMAL_BAM=${NORMAL_BAM_DIR}/${NORMAL_BAM}
    ARGUMNET="${ARGUMENT} --matched_control_bam ${NORMAL_BAM}"

    if [ ! _${CONTROL_PANEL} = "_None" ]
    then
        ARGUMNET="${ARGUMENT} --matched_control_label ${NORMAL_SAMPLE}"
    fi
fi

ARGUMENT="${ARGUMENT} ${GENOMONSV_FILT_OPTION}"

GenomonSV filt ${ARGUMENT}

sed -i "1i${META}" ${TUMOR_SV_DIR}/${TUMOR_SAMPLE}.genomonSV.result.txt

sv_utils filter ${TUMOR_SV_DIR}/${TUMOR_SAMPLE}.genomonSV.result.txt ${TUMOR_SV_DIR}/${TUMOR_SAMPLE}.genomonSV.result.filt.txt ${SV_UTILS_FILT_OPTION}

