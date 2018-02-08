#!/bin/bash

# set -o errexit
set -o nounset

# format

input_dir=`realpath $(dirname ${INPUT_MUTATION1})/..`
merged=${OUTPUT_DIR}/mutation_cut.${MODE}.txt

for mutation_file in `ls ${input_dir}/*/*.genomon_mutation.result.filt.txt`
do
    if [ `cat ${mutation_file} | grep -P '^[^#]' | wc -l` -gt 1 ]; then
    
        sample=`basename ${mutation_file} | sed -e "s/.genomon_mutation.result.filt.txt//;"`
        cat ${mutation_file} | sed -e "s/^/${sample}\t/g" > ${merged}.named
        cut -s -f 1,2,3,5,6 ${merged}.named | tail -n +2 | grep -P '^[^\t]+\t([Cc]hr)?[0-9XY]' > ${merged}.cut
        
        cut -s -f 1 ${merged}.cut > ${merged}.cut1
        cut -s -f 2 ${merged}.cut | sed "s/^/chr/" | sed -e "s/^chr[Cc]hr/chr/g" > ${merged}.cut2
        cut -s -f 3,4,5 ${merged}.cut > ${merged}.cut3
        paste ${merged}.cut1 ${merged}.cut2 ${merged}.cut3 >> ${merged}.tmp
        rm ${merged}.named ${merged}.cut ${merged}.cut1 ${merged}.cut2 ${merged}.cut3
    fi
done

if [ -e ${merged}.tmp ]; then
    mv ${merged}.tmp ${merged}
else
    touch ${merged}
fi

# pmsignature (ind) / signature (full)

output_pre=${OUTPUT_DIR}/pmsignature

for signum in `seq ${SIG_MIN} ${SIG_MAX}`
do
    R --vanilla --slave --args ${merged} ${output_pre}.${signum}.${MODE}.RData ${signum} ${TRDIRFLAG} ${TRIALNUM} ${BGFLAG} ${BS_GENOME} ${TXDB_TRANSCRIPT} < /tools/genomon_Rscripts-0.1.3/pmsignature/run_pmsignature_${MODE}.R
    if [ $? -ne 0 ]
    then
        echo pmsignature terminated abnormally.
        if [ ${MODE} = "ind" ]
        then
            echo '{{"id":[],"ref":[],"alt":[],"strand":[],"mutation":[]}}' > ${output_pre}.${MODE}.result.${signum}.json
        else
            echo '{{"id":[],"signature":[],"mutation":[]}}' > ${output_pre}.${MODE}.result.${signum}.json
        fi
    else
        R --vanilla --slave --args ${output_pre}.${signum}.${MODE}.RData ${output_pre}.${MODE}.result.${signum}.json < /tools/genomon_Rscripts-0.1.3/pmsignature/convert_toJson_${MODE}.R
    fi
done
