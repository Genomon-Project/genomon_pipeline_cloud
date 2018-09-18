#!/bin/bash

set -o errexit
set -o nounset

OUTPUT_PREF=${OUTPUT_DIR}/${SAMPLE}
mkdir -p ${OUTPUT_DIR}

if [ "${INPUT_BAM-UNDEF}" != "UNDEF" ]; then
    if [ "$INPUT_BAM" != "" ]; then
        FASTQ1=${OUTPUT_PREF}.sequence1.fastq
        FASTQ2=${OUTPUT_PREF}.sequence2.fastq
        SUMMARYTXT=${OUTPUT_PREF}.bamtofastq.summary.txt

        /usr/local/bin/bamtofastq ${BAMTOFASTQ_OPTION} \
            filename=${INPUT_BAM} \
            F=${FASTQ1} \
            F2=${FASTQ2} \
            T=${OUTPUT_PREF}.temp.txt \
            S=${OUTPUT_PREF}.single.txt \
            O=${OUTPUT_PREF}.orphans1.txt \
            O2=${OUTPUT_PREF}.orphans2.txt 2>&1 | tee $SUMMARYTXT.tmp

        grep -E "^\[C\]" $SUMMARYTXT.tmp > $SUMMARYTXT
        rm $SUMMARYTXT.tmp
        rm ${OUTPUT_PREF}.single.txt
        rm ${OUTPUT_PREF}.orphans1.txt
        rm ${OUTPUT_PREF}.orphans2.txt
    fi
fi

/usr/local/bin/STAR \
    --genomeDir ${REFERENCE} \
    --readFilesIn ${FASTQ1} ${FASTQ2} \
    --outFileNamePrefix ${OUTPUT_PREF}. \
    ${STAR_OPTION}

rm $FASTQ1
rm $FASTQ2

/usr/local/bin/samtools sort \
    -T ${OUTPUT_PREF}.Aligned.sortedByCoord.out \
    ${SAMTOOLS_SORT_OPTION} \
    ${OUTPUT_PREF}.Aligned.out.bam \
    -O bam > ${OUTPUT_PREF}.Aligned.sortedByCoord.out.bam

/usr/local/bin/samtools index \
    ${OUTPUT_PREF}.Aligned.sortedByCoord.out.bam

rm ${OUTPUT_PREF}.Aligned.out.bam

