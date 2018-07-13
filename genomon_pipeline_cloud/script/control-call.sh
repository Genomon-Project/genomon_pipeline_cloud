#!/bin/bash

set -o errexit
set -o nounset

export PATH=/usr/local/bin:${PATH}
export LD_LIBRARY_PATH=/usr/local/lib
OUTPUT_PREF=${OUTPUT_DIR}/${SAMPLE}
REFERENCE=${REFERENCE}/GRCh37.fa

# INPUT_BAM1: target
INPUT_BAM=${INPUT_DIR}/${SAMPLE}.markdup.bam

# Fisher's Exact Test
if [ "_${FISHER_SINGLE_SAMTOOLS}" != "_" ]; then
    FISHER_SINGLE_OPTION="${FISHER_SINGLE_OPTION} --samtools_params "
fi
fisher single -O vcf -o ${OUTPUT_PREF}.control.vcf --ref_fa ${REFERENCE} -1 ${INPUT_BAM} --samtools_path samtools ${FISHER_SINGLE_OPTION} "${FISHER_SINGLE_SAMTOOLS}"

bgzip ${OUTPUT_PREF}.control.vcf 
tabix ${OUTPUT_PREF}.control.vcf.gz 
