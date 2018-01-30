#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace

export bamstats=/tools/ICGC/bin/bam_stats.pl
export bedtools=/usr/local/bin/bedtools
export ld_library_path=/usr/local/bin
export perl5lib=/tools/ICGC/lib/perl5:/tools/ICGC/lib/perl5/x86_64-linux-gnu-thread-multi
export samtools=/usr/local/bin/samtools

input_file=${INPUT_DIR}/${SAMPLE}.markdup.bam
output_pre=${OUTPUT_DIR}/${SAMPLE}

# bamstats
genomon_qc bamstats $input_file $output_pre.bamstats \
    --perl5lib $perl5lib \
    --bamstats $bamstats

# coverage
if [ ${DATA_TYPE} = "wgs" ]
then
    genomon_qc wgs $input_file $output_pre.coverage \
        --genome_size_file ${GENOME_SIZE_FILE} \
        --gaptxt ${GAPTXT} \
        --incl_bed_width ${INCL_BED_WIDTH} \
        --i_bed_lines ${I_BED_LINES} \
        --i_bed_width ${I_BED_WIDTH} \
        --ld_library_path ${ld_library_path} \
        --bedtools $bedtools \
        --samtools $samtools \
        --samtools_params "${SAMTOOLS_PARAMS}" \
        --coverage_text ${COVERAGE_TEXT} \
        --del_tempfile True

else
    genomon_qc exome $input_file $output_pre.coverage \
        --bait_file ${BAIT_FILE} \
        --ld_library_path $ld_library_path \
        --bedtools $bedtools \
        --samtools $samtools \
        --samtools_params "${SAMTOOLS_PARAMS}" \
        --coverage_text ${COVERAGE_TEXT} \
        --del_tempfile True
fi

# merge
if [ -f ${FASTQ_LINE_NUM_FILE} ]; then

    total_reads=`awk 'NR==2 {print $15}' $output_pre.bamstats`
    fastq_reads_tmp=`cat ${FASTQ_LINE_NUM_FILE}`
    fastq_reads=`expr $fastq_reads_tmp / 2`

    if [ $total_reads -ne $fastq_reads ]; then
        echo "Total read count is not good for this data. BAM file: $total_reads reads. FASTQ file: $fastq_reads reads." >&2
        exit 1
    fi
fi

genomon_qc merge $output_pre.coverage $output_pre.bamstats $output_pre.genomonQC.result.txt --meta "${META}"

