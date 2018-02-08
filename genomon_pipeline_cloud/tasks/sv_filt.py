#! /usr/bin/env python

import pkg_resources
from ..abstract_task import *
 
class SV_filt(Abstract_task):

    task_name = "sv-filt"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(SV_filt, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            param_conf.get("sv_filt", "image"),
            param_conf.get("sv_filt", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        # generate fusionfusion_tasks.tsv
        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:
            
            print >> hout, '\t'.join(["--env TUMOR_SAMPLE",
                                      "--env NORMAL_SAMPLE",
                                      "--env CONTROL_PANEL",
                                      "--input-recursive TUMOR_BAM_DIR",
                                      "--input-recursive TUMOR_SV_DIR",
                                      "--input-recursive NORMAL_BAM_DIR",
                                      "--env META",
                                      "--input REFERENCE",
                                      "--input MERGED_JUNCTION",
                                      "--output-recursive OUTPUT_DIR",
                                      "--env GENOMONSV_FILT_OPTION",
                                      "--env SV_UTILS_FILT_OPTION"])
    
            for tumor_sample, normal_sample, control_panel_name in sample_conf.sv_detection:

                print >> hout, '\t'.join([str(tumor_sample),
                                          str(normal_sample),
                                          str(control_panel_name),
                                          output_dir + "/bam/" + tumor_sample,
                                          output_dir + "/sv/" + tumor_sample,
                                          output_dir + "/bam/" + normal_sample if normal_sample is not None else '',
                                          run_conf.get_meta_info(param_conf.get("sv_filt", "image")),
                                          param_conf.get("sv_filt", "reference"),
                                          '',
                                          output_dir + "/sv/" + tumor_sample,
                                          param_conf.get("sv_filt", "genomon_sv_filt_option"),
                                          param_conf.get("sv_filt", "sv_utils_filt_option")])

        return task_file

