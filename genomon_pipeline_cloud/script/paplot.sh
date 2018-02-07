#!/bin/bash

set -o errexit
# set -o nounset
set -o xtrace

# rna

if test -n "${INPUT_STARQC1}"
then
    dir_starqc=`realpath $(dirname ${INPUT_STARQC1})/..`
    for input in `ls ${dir_starqc}/*/*.Log.final.out`
    do
        while read line
        do
            h=`echo ${line} | sed -e "s/ | /|/" | cut -f 1 -d \| -s`
            d=`echo ${line} | sed -e "s/ | /|/" | cut -f 2 -d \| -s | sed -e "s/%//"`
    
            if test -n "$h";
            then
                if test -n "$header";
                then
                    header=${header}'\t'$h
                    data=${data}'\t'$d
                else
                    header=$h
                    data=$d
                fi
            fi
        done < ${input} 
    
        tempfile=${input}.tsv
        #tempfile=${OUTPUT_DIR}/`basename ${input}`.tsv
        
        echo "$header" > ${tempfile}
        echo "$data" >> ${tempfile}
        
        if test -n "$input_starqc_tsv";
        then
            input_starqc_tsv=${input_starqc_tsv},${tempfile}
        else
            input_starqc_tsv=${tempfile}
        fi
    done
    
    paplot qc ${input_starqc_tsv} ${OUTPUT_DIR} ${TITLE} --config_file ${CONFIG_FILE} --title 'QC graphs' --overview 'Quality Control of bam.' --ellipsis qc
fi

if test -n "${INPUT_FUSION1}"
then
    dir_fusion=`realpath $(dirname ${INPUT_FUSION1})/..`
    paplot ca "${dir_fusion}/*/*.genomonFusion.result.filt.txt" ${OUTPUT_DIR} ${TITLE} --config_file ${CONFIG_FILE} --title 'Fusion graphs' --overview 'Fusion.' --ellipsis fusion
fi

# dna

if test -n "${INPUT_QC1}"
then
    dir_qc=`realpath $(dirname ${INPUT_QC1})/..`
    paplot qc "${dir_qc}/*/*.genomonQC.result.txt" ${OUTPUT_DIR} ${TITLE} --config_file ${CONFIG_FILE} --title 'QC graphs' --overview 'Quality Control of bam.' --ellipsis qc
fi

if test -n "${INPUT_SV1}"
then
    dir_sv=`realpath $(dirname ${INPUT_SV1})/..`
    paplot ca "${dir_sv}/*/*.genomonSV.result.filt.txt" ${OUTPUT_DIR} ${TITLE} --config_file ${CONFIG_FILE} --title 'SV graphs' --overview 'Structural Variation.' --ellipsis sv 
fi

if test -n "${INPUT_MUTATION1}"
then
    dir_mutation=`realpath $(dirname ${INPUT_MUTATION1})/..`
    paplot mutation " ${dir_mutation}/*/*.genomon_mutation.result.filt.txt" ${OUTPUT_DIR} ${TITLE} --config_file ${CONFIG_FILE} --title 'Mutation matrix' --overview 'Gene-sample mutational profiles.' --ellipsis mutation
fi

if test -n "${INPUT_FULL1}"
then
    dir_signature=`realpath $(dirname ${INPUT_FULL1})/..`
    for input in `ls ${dir_signature}/*/pmsignature.full.result.*.json`
    do
        paplot signature $input ${OUTPUT_DIR} ${TITLE} --config_file ${CONFIG_FILE} --title 'Mutational Signature' --overview 'Pmsignature type=full.' --ellipsis full
    done
fi

if test -n "${INPUT_IND1}"
then
    dir_pmsignature=`realpath $(dirname ${INPUT_IND1})/..`
    for input in `ls ${dir_pmsignature}/*/pmsignature.ind.result.*.json`
    do
        paplot pmsignature $input ${OUTPUT_DIR} ${TITLE} --config_file ${CONFIG_FILE} --title 'pmsignature' --overview 'Pmsignature type=ind.' --ellipsis ind
    done
fi

# index

paplot index ${OUTPUT_DIR} --config_file ${CONFIG_FILE} --remarks "${REMARKS}"

real_output=`realpath ${OUTPUT_DIR}`
tar -zcvf ${real_output}/paplot.tar.gz ${real_output}/
