#!/bin/bash

set -o errexit
set -o nounset

export PATH=/usr/local/bin:${PATH}
export LD_LIBRARY_PATH=/usr/local/lib
OUTPUT_PREF=${OUTPUT_DIR}/${SAMPLE1}
REFERENCE=${REFERENCE}/GRCh37.fa
SAMTOOLS=/usr/local/bin/samtools
BLAT=/tools/userApps/bin/blat

# INPUT_BAM1: target
INPUT_BAM1=${INPUT_DIR1}/${SAMPLE1}.markdup.bam

if [ _${SAMPLE2} = "_None" ]; then 

    # Fisher's Exact Test
    option1=`echo ${FISHER_SINGLE_OPTION} | cut -d "'" -f 1`
    option2=`echo ${FISHER_SINGLE_OPTION} | cut -d "'" -f 2`
    fisher single -o ${OUTPUT_PREF}.fisher_mutations.txt --ref_fa ${REFERENCE} -1 ${INPUT_BAM1} --samtools_path ${SAMTOOLS} ${option1} "${option2}"

    # Local realignment using blat. The candidate mutations are varidated.
    mutfilter realignment --target_mutation_file ${OUTPUT_PREF}.fisher_mutations.txt -1 ${INPUT_BAM1} --output ${OUTPUT_PREF}.realignment_mutations.txt --ref_genome ${REFERENCE} --blat_path ${BLAT} ${REALIGNMENT_OPTION}

    # Annotation if the candidate is on the simplerepeat. 
    mutfilter simplerepeat --target_mutation_file ${OUTPUT_PREF}.realignment_mutations.txt --output ${OUTPUT_PREF}.simplerepeat_mutations.txt --simple_repeat_db ${ANNOTATION_DB}/simpleRepeat.bed.gz

else
    # INPUT_BAM2: pair
    INPUT_BAM2=${INPUT_DIR2}/${SAMPLE2}.markdup.bam

    # Fisher's Exact Test
    option1=`echo ${FISHER_PAIR_OPTION} | cut -d "'" -f 1`
    option2=`echo ${FISHER_PAIR_OPTION} | cut -d "'" -f 2`
    fisher comparison -o ${OUTPUT_PREF}.fisher_mutations.txt --ref_fa ${REFERENCE} -1 ${INPUT_BAM1} -2 ${INPUT_BAM2} --samtools_path ${SAMTOOLS} ${option1} "${option2}"
    
    # Identifying mutations in cancer hotspot
    option1=`echo ${HOTSPOT_OPTION} | cut -d "'" -f 1`
    option2=`echo ${HOTSPOT_OPTION} | cut -d "'" -f 2`
    hotspotCall ${option1} "${option2}" ${INPUT_BAM1} ${INPUT_BAM2} ${OUTPUT_PREF}.hotspot_mutations.txt ${HOTSPOT_DB}/GRCh37_hotspot_database_v20170919.txt 
    mutil merge_hotspot -i ${OUTPUT_PREF}.hotspot_mutations.txt -f ${OUTPUT_PREF}.fisher_mutations.txt -o ${OUTPUT_PREF}.fisher_hotspot_mutations.txt --hotspot_header
    
    # Local realignment using blat. The candidate mutations are varidated.
    mutfilter realignment --target_mutation_file ${OUTPUT_PREF}.fisher_hotspot_mutations.txt -1 ${INPUT_BAM1} -2 ${INPUT_BAM2} --output ${OUTPUT_PREF}.realignment_mutations.txt --ref_genome ${REFERENCE} --blat_path ${BLAT} ${REALIGNMENT_OPTION}
    
    # Annotation if the candidate is near Indel. 
    option1=`echo ${INDEL_OPTION} | cut -d "'" -f 1`
    option2=`echo ${INDEL_OPTION} | cut -d "'" -f 2`
    mutfilter indel --target_mutation_file ${OUTPUT_PREF}.realignment_mutations.txt -2 ${INPUT_BAM2} --output ${OUTPUT_PREF}.indel_mutations.txt --samtools_path ${SAMTOOLS} ${option1} "${option2}"
    
    # Annotation if the candidate is near the breakpoint. 
    mutfilter breakpoint --target_mutation_file ${OUTPUT_PREF}.indel_mutations.txt -2 ${INPUT_BAM2} --output ${OUTPUT_PREF}.breakpoint_mutations.txt ${BREAKPOINT_OPTION}
    
    # Annotation if the candidate is on the simplerepeat. 
    mutfilter simplerepeat --target_mutation_file ${OUTPUT_PREF}.breakpoint_mutations.txt --output ${OUTPUT_PREF}.simplerepeat_mutations.txt --simple_repeat_db ${ANNOTATION_DB}/simpleRepeat.bed.gz 
fi 

# HGVD annotations
if [ _${ACTIVE_HGVD_2016_FLAG} = "_True" ]; then 
    mutanno mutation -t ${OUTPUT_PREF}.simplerepeat_mutations.txt -o ${OUTPUT_PREF}.HGVD_2016.txt -d ${ANNOTATION_DB}/DBexome20160412.bed.gz -c 5
else
    cp ${OUTPUT_PREF}.simplerepeat_mutations.txt ${OUTPUT_PREF}.HGVD_2016.txt
fi
# ExAC annotations
if [ _${ACTIVE_EXAC_FLAG} = "_True" ]; then 
    mutanno mutation -t ${OUTPUT_PREF}.HGVD_2016.txt -o ${OUTPUT_PREF}.ExAC.txt -d ${ANNOTATION_DB}/ExAC.r0.3.1.sites.vep.bed.gz -c 8
else
    cp ${OUTPUT_PREF}.HGVD_2016.txt ${OUTPUT_PREF}.ExAC.txt
fi

cp ${OUTPUT_PREF}.ExAC.txt ${OUTPUT_PREF}.mutations_candidate.txt

# Add header
mut_header=""
if [ _${SAMPLE2} = "_None" ]
then
    mut_header="Chr,Start,End,Ref,Alt,depth,variantNum,bases,A_C_G_T,misRate,strandRatio,10%_posterior_quantile,posterior_mean,90%_posterior_quantile,readPairNum,variantPairNum,otherPairNum,10%_posterior_quantile(realignment),posterior_mean(realignment),90%_posterior_quantile(realignment),simple_repeat_pos,simple_repeat_seq,P-value(EBCall)"
else
    mut_header="Chr,Start,End,Ref,Alt,depth_tumor,variantNum_tumor,depth_normal,variantNum_normal,bases_tumor,bases_normal,A_C_G_T_tumor,A_C_G_T_normal,misRate_tumor,strandRatio_tumor,misRate_normal,strandRatio_normal,P-value(fisher),score(hotspot),readPairNum_tumor,variantPairNum_tumor,otherPairNum_tumor,readPairNum_normal,variantPairNum_normal,otherPairNum_normal,P-value(fisher_realignment),indel_mismatch_count,indel_mismatch_rate,bp_mismatch_count,distance_from_breakpoint,simple_repeat_pos,simple_repeat_seq,P-value(EBCall)"
fi

if [ _${CONTROL_BAM_LIST} = "_None" ]
then
    mut_header=`echo ${mut_header} | awk -F"," -v OFS="," '{{$NF=""; sub(/.$/,""); print $0}}'`
fi

tmp_header=`echo $mut_header | tr "," "\t"`
print_header=${tmp_header}

if [ _${ACTIVE_HGVD_2016_FLAG} = "_True" ]
then
    HGVD_header="HGVD_20160412:#Sample,HGVD_20160412:Filter,HGVD_20160412:NR,HGVD_20160412:NA,HGVD_20160412:Frequency(NA/(NA+NR))"
    tmp_header=`echo $HGVD_header | tr "," "\t"`
    print_header=${print_header}"\t"${tmp_header}
fi
if [ _${ACTIVE_EXAC_FLAG} = "_True" ]
then
    ExAC_header="ExAC:Filter,ExAC:AC_Adj,ExAC:AN_Adj,ExAC:Frequency(AC_Adj/AN_Adj),ExAC:AC_POPMAX,ExAC:AN_POPMAX,ExAC:Frequency(AC_POPMAX/AN_POPMAX),ExAC:POPMAX"
    tmp_header=`echo $ExAC_header | tr "," "\t"`
    print_header=${print_header}"\t"${tmp_header}
fi

echo "$META" > ${OUTPUT_PREF}.genomon_mutation.result.txt
echo "$print_header" >> ${OUTPUT_PREF}.genomon_mutation.result.txt
cat ${OUTPUT_PREF}.mutations_candidate.txt >> ${OUTPUT_PREF}.genomon_mutation.result.txt

# filter candidates
if [ _${SAMPLE2} = "_None" ]
then 
    mutil filter -i ${OUTPUT_PREF}.genomon_mutation.result.txt -o ${OUTPUT_PREF}.genomon_mutation.result.filt.txt ${FILTER_SINGLE_OPTION}
else
    mutil filter -i ${OUTPUT_PREF}.genomon_mutation.result.txt -o ${OUTPUT_PREF}.genomon_mutation.result.filt.txt ${FILTER_PAIR_OPTION} --hotspot_db ${HOTSPOT_DB}/GRCh37_hotspot_database_v20170919.txt
fi

rm -f ${OUTPUT_PREF}.ExAC.txt
rm -f ${OUTPUT_PREF}.HGVD_2016.txt
rm -f ${OUTPUT_PREF}.breakpoint_mutations.txt
rm -f ${OUTPUT_PREF}.fisher_hotspot_mutations.txt
rm -f ${OUTPUT_PREF}.fisher_mutations.txt
rm -f ${OUTPUT_PREF}.hotspot_mutations.txt
rm -f ${OUTPUT_PREF}.indel_mutations.txt
rm -f ${OUTPUT_PREF}.mutations_candidate.txt
rm -f ${OUTPUT_PREF}.realignment_mutations.txt
rm -f ${OUTPUT_PREF}.simplerepeat_mutations.txt

