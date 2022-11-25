#! /usr/bin/env python

import os
import genomon_pipeline_cloud.abstract_task as abstract_task
 
class SV_filt(abstract_task.Abstract_task):

    task_name = "sv-filt"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(SV_filt, self).__init__(
            self.__class__.task_name,
            param_conf.get("sv_filt", "image"),
            param_conf.get("sv_filt", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        # generate fusionfusion_tasks.tsv
        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:
            
            hout.write('\t'.join(["--env TUMOR_SAMPLE",
                                  "--env NORMAL_SAMPLE",
                                  "--env CONTROL_PANEL",
                                  "--input-recursive TUMOR_BAM_DIR",
                                  "--env TUMOR_BAM",
                                  "--input-recursive TUMOR_SV_DIR",
                                  "--input-recursive NORMAL_BAM_DIR",
                                  "--env NORMAL_BAM",
                                  "--env META",
                                  "--input REFERENCE",
                                  "--input-recursive MERGED_JUNCTION",
                                  "--output-recursive OUTPUT_DIR",
                                  "--env GENOMONSV_FILT_OPTION",
                                  "--env SV_UTILS_FILT_OPTION"])
                                  + "\n")
    
            for tumor_sample, normal_sample, control_panel_name in sample_conf.sv_detection:

                tumor_bam = sample_conf.bwa_bam_file[tumor_sample]
                tumor_bam_dir = os.path.dirname(tumor_bam)
                tumor_bam_file = os.path.basename(tumor_bam)

                normal_bam_dir = ""
                normal_bam_file = ""
                if normal_sample is not None:
                    normal_bam = sample_conf.bwa_bam_file[normal_sample]
                    normal_bam_dir = os.path.dirname(normal_bam)
                    normal_bam_file = os.path.basename(normal_bam)

                hout.write('\t'.join([str(tumor_sample),
                                      str(normal_sample),
                                      str(control_panel_name),
                                      tumor_bam_dir,
                                      tumor_bam_file,
                                      output_dir + "/sv/" + tumor_sample,
                                      normal_bam_dir,
                                      normal_bam_file,
                                      run_conf.get_meta_info(param_conf.get("sv_filt", "image")),
                                      param_conf.get("sv_filt", "reference"),
                                      output_dir + "/sv/control_panel/" + control_panel_name if control_panel_name is not None else '',
                                      output_dir + "/sv/" + tumor_sample,
                                      param_conf.get("sv_filt", "genomon_sv_filt_option"),
                                      param_conf.get("sv_filt", "sv_utils_filt_option")])
                                      + "\n")

        return task_file

