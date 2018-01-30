#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace

export LD_LIBRARY_PATH=/usr/local/lib
OUTPUT_PREF=${OUTPUT_DIR}/${SAMPLE}
REFERENCE=${REFERENCE}/GRCh37.fa

/tools/bwa-0.7.8/bwa mem ${BWA_OPTION} ${REFERENCE} ${INPUT1} ${INPUT2} | /usr/local/bin/bamsort ${BAMSORT_OPTION} calmdnmreference=${REFERENCE} tmpfile=${OUTPUT_PREF}.sorted.bam.tmp inputformat=sam indexfilename=${OUTPUT_PREF}.sorted.bam.bai O=${OUTPUT_PREF}.sorted.bam

/usr/local/bin/bammarkduplicates ${BAMMARKDUP_OPTION} M=${OUTPUT_PREF}.metrics tmpfile=${OUTPUT_PREF}.markdup.bam.tmp I=${OUTPUT_PREF}.sorted.bam O=${OUTPUT_PREF}.markdup.bam

rm ${OUTPUT_PREF}.sorted.bam
rm ${OUTPUT_PREF}.sorted.bam.bai

