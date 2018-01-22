#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace

OUTPUT_PREF=${OUTPUT_DIR}/${SAMPLE}

/usr/local/bin/STAR --genomeDir ${REFERENCE} --readFilesIn ${INPUT1} ${INPUT2} --outFileNamePrefix ${OUTPUT_PREF}. ${STAR_OPTION}

/usr/local/bin/samtools sort -T ${OUTPUT_PREF}.Aligned.sortedByCoord.out ${SAMTOOLS_SORT_OPTION} ${OUTPUT_PREF}.Aligned.out.bam -O bam > ${OUTPUT_PREF}.Aligned.sortedByCoord.out.bam

/usr/local/bin/samtools index ${OUTPUT_PREF}.Aligned.sortedByCoord.out.bam

rm -rf ${OUTPUT_PREF}.Aligned.out.bam


