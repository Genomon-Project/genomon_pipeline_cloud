#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace

TUMOR_BAM=${TUMOR_BAM_DIR}/${TUMOR_SAMPLE}.markdup.bam

ARGUMENT="${TUMOR_BAM} ${TUMOR_SV_DIR}/${TUMOR_SAMPLE} ${REFERENCE}"

if [ !_${CONTROL_PANEL} = "_None" ]
then
    ARGUMENT="${ARGUMENT} --non_matched_control_junction ${MERGED_JUNCTION}"
fi

if [ ! _${NORMAL_SAPLE} = "_None" ]
then
    NORMAL_BAM=${NORMAL_BAM_DIR}/${NORMAL_SAMPLE}.markdup.bam
    ARGUMNET="${ARGUMENT} --matched_control_bam ${NORMAL_BAM}"

    if [ !_${CONTROL_PANEL} = "_None" ]
    then
        ARGUMNET="${ARGUMENT} --matched_control_label ${NORMAL_SAMPLE}"
    fi
fi

GenomonSV filt ${ARGUMENT}
 
