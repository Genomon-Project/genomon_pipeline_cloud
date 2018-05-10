#!/bin/bash

set -o errexit
set -o nounset

export LD_LIBRARY_PATH=/usr/local/lib
OUTPUT_PREF=${OUTPUT_DIR}/${SAMPLE}
REFERENCE=${REFERENCE}/GRCh37.fa

if [ "${INPUT_BAM-UNDEF}" != "UNDEF" ]; then
    if [ "$INPUT_BAM" != "" ]; then
        FASTQ1=${OUTPUT_PREF}.sequence1.fastq
        FASTQ2=${OUTPUT_PREF}.sequence2.fastq
        TEMPTXT=${OUTPUT_PREF}.temp.txt
        SINGLETXT=${OUTPUT_PREF}.single.txt
        ORPHANS1=${OUTPUT_PREF}.orphans1.txt
        ORPHANS2=${OUTPUT_PREF}.orphans2.txt
        SUMMARYTXT=${OUTPUT_PREF}.bamtofastq.summary.txt
        /usr/local/bin/bamtofastq ${BAMTOFASTQ_OPTION} filename=${INPUT_BAM} F=${FASTQ1} F2=${FASTQ2} T=${TEMPTXT} S=${SINGLETXT} O=${ORPHANS1} O2=${ORPHANS2} 2>&1 | tee $SUMMARYTXT.tmp
        grep -E "^\[C\]" $SUMMARYTXT.tmp > $SUMMARYTXT
        rm $SUMMARYTXT.tmp
        rm $SINGLETXT
        rm $ORPHANS1
        rm $ORPHANS2
    fi
fi
/tools/bwa-0.7.8/bwa mem ${BWA_OPTION} ${REFERENCE} ${FASTQ1} ${FASTQ2} | /usr/local/bin/bamsort ${BAMSORT_OPTION} calmdnmreference=${REFERENCE} inputformat=sam indexfilename=${OUTPUT_PREF}.sorted.bam.bai O=${OUTPUT_PREF}.sorted.bam

rm $FASTQ1
rm $FASTQ2

/usr/local/bin/bammarkduplicates ${BAMMARKDUP_OPTION} M=${OUTPUT_PREF}.metrics I=${OUTPUT_PREF}.sorted.bam O=${OUTPUT_PREF}.markdup.bam

rm ${OUTPUT_PREF}.sorted.bam
rm ${OUTPUT_PREF}.sorted.bam.bai
