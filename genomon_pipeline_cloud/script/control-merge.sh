#!/bin/bash

set -o errexit

export PATH=/usr/local/bin:${PATH}
export LD_LIBRARY_PATH=/usr/local/lib
OUTPUT_PREF=${OUTPUT_DIR}/${PANEL_NAME}

TARGET_VCF=""
count=0
for i in `seq 1 $MAX_COUNT`; do
    TMP_INPUT_DIR=$(eval echo \$INPUT_DIR_${i}) 
    if [ "${TMP_INPUT_DIR-UNDEF}" != "UNDEF" ]; then
        if [ "$TMP_INPUT_DIR" != "" ]; then
            SAMPLE=`echo ${TMP_INPUT_DIR} | awk -F "/" '{ print $NF }'`
            VCF_FILE=${TMP_INPUT_DIR}/${SAMPLE}.control.vcf.gz
            TARGET_VCF="$TARGET_VCF $VCF_FILE"
            count=$(expr $count + 1)
        fi
    fi
done

if [ $count -gt 1 ]; then
    bcftools merge ${BCFTOOLS_OPTION} -o ${OUTPUT_PREF}.merged_control.vcf.gz $TARGET_VCF 
else
    cp $TARGET_VCF ${OUTPUT_PREF}.merged_control.vcf.gz
fi
tabix ${OUTPUT_PREF}.merged_control.vcf.gz 
