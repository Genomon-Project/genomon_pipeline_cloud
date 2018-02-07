#! /usr/bin/env python

import pkg_resources
from ..abstract_task import *
 
class SV_parse(Abstract_task):

    task_name = "sv-parse"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(SV_parse, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            param_conf.get("sv_parse", "image"),
            param_conf.get("sv_parse", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        # generate fusionfusion_tasks.tsv
        #task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:
            
            print >> hout, '\t'.join(["--env SAMPLE",
                                      "--input-recursive INPUT_DIR",
                                      "--output-recursive OUTPUT_DIR",
                                      "--env OPTION"])
    
            # List up the sample list
            sample_list_for_parse = []
            for tumor_sample, normal_sample, control_panel_name in sample_conf.sv_detection:
                sample_list_for_parse.append(tumor_sample)
                if normal_sample is not None: sample_list_for_parse.append(normal_sample)
                if control_panel_name is not None: sample_list_for_parse = sample_list_for_parse + sample_conf.control_panel[control_panel_name]
            
            sample_list_for_parse = list(set(sample_list_for_parse))

            for sample_name in sorted(sample_list_for_parse):
                if sample_name in sample_conf.bam_tofastq.keys() + sample_conf.fastq.keys():
                    print >> hout, '\t'.join([sample_name,
                                              output_dir + "/bam/" + sample_name,
                                              output_dir + "/sv/" + sample_name,
                                              param_conf.get("sv_parse", "genomon_sv_parse_option")])
                elif sample_name in sample_conf.bam_import.keys():
                    raise NotImplementedError("sv_parse for bam_import is not implemented: " + sample_name)
                else:
                    raise ValueError(sample_name + " is not registered in any of [fastq], [bam_tofastq], [bam_import]") 

        return task_file

