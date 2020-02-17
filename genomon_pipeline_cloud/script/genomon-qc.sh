#!/bin/bash

set -o errexit
set -o nounset

export bamstats=/tools/ICGC/bin/bam_stats.pl
export bedtools=/usr/local/bin/bedtools
export ld_library_path=/usr/local/bin
export perl5lib=/tools/ICGC/lib/perl5:/tools/ICGC/lib/perl5/x86_64-linux-gnu-thread-multi
export samtools=/usr/local/bin/samtools

input_file=${INPUT_DIR}/${INPUT_BAM}
output_pre=${OUTPUT_DIR}/${SAMPLE}

mkdir -p ${OUTPUT_DIR}

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
        ${GRC_FLAG} \
        --del_tempfile

else
    genomon_qc exome $input_file $output_pre.coverage \
        --bait_file ${BAIT_FILE} \
        --ld_library_path $ld_library_path \
        --bedtools $bedtools \
        --samtools $samtools \
        --samtools_params "${SAMTOOLS_PARAMS}" \
        --coverage_text ${COVERAGE_TEXT} \
        --del_tempfile
fi

# merge
genomon_qc merge $output_pre.coverage $output_pre.bamstats $output_pre.genomonQC.result.txt --meta "${META}"

