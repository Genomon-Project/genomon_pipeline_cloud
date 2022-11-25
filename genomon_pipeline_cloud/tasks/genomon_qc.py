#! /usr/bin/env python

import os
import genomon_pipeline_cloud.abstract_task as abstract_task
 
class Genomon_qc(abstract_task.Abstract_task):

    task_name = "genomon-qc"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Genomon_qc, self).__init__(
            self.__class__.task_name,
            param_conf.get("qc", "image"),
            param_conf.get("qc", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        data_type = "exome"
        if param_conf.get("qc", "wgs_flag") == "True":
            data_type = "wgs"
        
        #task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            hout.write('\t'.join(["--env SAMPLE",
                                  "--input-recursive INPUT_DIR",
                                  "--env INPUT_BAM",
                                  "--output-recursive OUTPUT_DIR",
                                  "--input BAIT_FILE",
                                  "--input GAPTXT",
                                  "--env GENOME_SIZE_FILE",
                                  "--env META",
                                  "--env DATA_TYPE",
                                  "--env COVERAGE_TEXT",
                                  "--env INCL_BED_WIDTH",
                                  "--env I_BED_LINES",
                                  "--env I_BED_WIDTH",
                                  "--env GRC_FLAG",
                                  "--env SAMTOOLS_PARAMS"]) 
                                  + "\n")

            for sample in sample_conf.qc:

                bam = sample_conf.bwa_bam_file[sample]
                bam_dir = os.path.dirname(bam)
                bam_file = os.path.basename(bam)
                
                param_grc_flag = ""
                grc_flag = "false"
                if "grc_flag" in param_conf.options("qc"):
                    grc_flag = param_conf.get("qc", "grc_flag")
                if grc_flag.lower() == "true":
                    param_grc_flag = "--grc_flag"
                
                hout.write('\t'.join([sample,
                                      bam_dir,
                                      bam_file,
                                      output_dir + "/qc/" + sample,
                                      param_conf.get("qc", "bait_file"),
                                      param_conf.get("qc", "gaptxt"),
                                      param_conf.get("qc", "genome_size_file"),
                                      run_conf.get_meta_info(param_conf.get("qc", "image")),
                                      data_type,
                                      param_conf.get("qc", "coverage_text"),
                                      param_conf.get("qc", "wgs_incl_bed_width"),
                                      param_conf.get("qc", "wgs_i_bed_lines"),
                                      param_conf.get("qc", "wgs_i_bed_width"),
                                      param_grc_flag,
                                      param_conf.get("qc", "samtools_params")]) 
                                      + "\n")

        return task_file

