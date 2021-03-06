#! /usr/bin/env python

import os
import genomon_pipeline_cloud.abstract_task as abstract_task
 
class Mutation_call(abstract_task.Abstract_task):

    task_name = "mutation-call"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Mutation_call, self).__init__(
            self.__class__.task_name,
            param_conf.get("mutation_call", "image"),
            param_conf.get("mutation_call", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            hout.write('\t'.join(["--env SAMPLE1",
                                  "--env SAMPLE2",
                                  "--env CONTROL_BAM_LIST",
                                  "--input-recursive INPUT_DIR1",
                                  "--input-recursive INPUT_DIR2",
                                  "--env INPUT_BAM1",
                                  "--env INPUT_BAM2",
                                  "--output-recursive OUTPUT_DIR",
                                  "--env META",
                                  "--input REFERENCE",
                                  "--input REFERENCE_INDEX",
                                  "--input HOTSPOT_DB",
                                  "--input-recursive ANNOTATION_DB",
                                  "--env FISHER_SINGLE_OPTION",
                                  "--env FISHER_SINGLE_SAMTOOLS",
                                  "--env FISHER_PAIR_OPTION",
                                  "--env FISHER_PAIR_SAMTOOLS",
                                  "--input FISHER_INTERVAL_LIST",
                                  "--env HOTSPOT_OPTION",
                                  "--env HOTSPOT_SAMTOOLS",
                                  "--env REALIGNMENT_OPTION",
                                  "--env INDEL_OPTION",
                                  "--env INDEL_SAMTOOLS",
                                  "--env BREAKPOINT_OPTION",
                                  "--env FILTER_PAIR_OPTION",
                                  "--env FILTER_SINGLE_OPTION",
                                  "--env ACTIVE_HGVD_2016_FLAG",
                                  "--env ACTIVE_EXAC_FLAG"]) 
                                  + "\n")

            for sample in sample_conf.mutation_call:

                sample_tumor = sample[0]
                sample_normal = sample[1] if sample[1] != None else "None"
                control_panel = sample[2] if sample[2] != None else "None"

                tumor_bam = sample_conf.bam_file[sample_tumor]
                tumor_bam_dir = os.path.dirname(tumor_bam)
                tumor_bam_file = os.path.basename(tumor_bam)
                
                normal_bam_dir = "" 
                normal_bam_file = "" 
                if sample_normal != "None": 
                    normal_bam = sample_conf.bam_file[sample_normal]
                    normal_bam_dir = os.path.dirname(normal_bam)
                    normal_bam_file = os.path.basename(normal_bam)

                hout.write('\t'.join([sample_tumor,
                                      sample_normal,
                                      control_panel,
                                      tumor_bam_dir,
                                      normal_bam_dir,
                                      tumor_bam_file,
                                      normal_bam_file,
                                      output_dir + "/mutation/" + sample_tumor,
                                      run_conf.get_meta_info(param_conf.get("mutation_call", "image")),
                                      param_conf.get("mutation_call", "reference"),
                                      param_conf.get("mutation_call", "reference_idx"),
                                      param_conf.get("mutation_call", "hotspot_database"),
                                      param_conf.get("mutation_call", "annotation_database"),
                                      param_conf.get("mutation_call", "fisher_single_option"),
                                      param_conf.get("mutation_call", "fisher_single_samtools"),
                                      param_conf.get("mutation_call", "fisher_pair_option"),
                                      param_conf.get("mutation_call", "fisher_pair_samtools"),
                                      param_conf.get("mutation_call", "fisher_interval_list"),
                                      param_conf.get("mutation_call", "hotspot_call_option"),
                                      param_conf.get("mutation_call", "hotspot_call_samtools"),
                                      param_conf.get("mutation_call", "realignment_option"),
                                      param_conf.get("mutation_call", "indel_option"),
                                      param_conf.get("mutation_call", "indel_samtools"),
                                      param_conf.get("mutation_call", "breakpoint_option"),
                                      param_conf.get("mutation_call", "filter_pair_option"),
                                      param_conf.get("mutation_call", "filter_single_option"),
                                      param_conf.get("mutation_call", "active_hgvd_2016_flag"),
                                      param_conf.get("mutation_call", "active_exac_flag")]) 
                                      + "\n")

        return task_file

