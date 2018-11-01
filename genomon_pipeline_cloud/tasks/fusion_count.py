#! /usr/bin/env python

import os
import pkg_resources
from ..abstract_task import *
 
class Fusion_count(Abstract_task):

    task_name = "fusion-count"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Fusion_count, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            param_conf.get("fusion_count_control", "image"),
            param_conf.get("fusion_count_control", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            print >> hout, '\t'.join(["--env SAMPLE",
                                      "--input INPUT",
                                      "--output-recursive OUTPUT_DIR",
                                      "--env META",
                                      "--env OPTION"])

            control_panel_li = []
            for tumor_sample, panel_name  in sample_conf.fusion:
                if panel_name != None: control_panel_li.append(panel_name)
            control_panel_li_uniq = list(set(control_panel_li))
           
            control_sample_li = [] 
            for panel_name in sample_conf.control_panel:
                if panel_name in control_panel_li_uniq: control_sample_li.extend(sample_conf.control_panel[panel_name])
            control_sample_li_uniq = list(set(control_sample_li))

            for sample in control_sample_li_uniq:

                bam = sample_conf.bam_file[sample]
                bam_dir = os.path.dirname(bam)

                print >> hout, '\t'.join([sample,
                                          bam_dir + "/" + sample + ".Chimeric.out.sam",
                                          output_dir + "/fusion/control_panel/" + sample,
                                          run_conf.get_meta_info(param_conf.get("fusion_count_control", "image")),
                                          param_conf.get("fusion_count_control", "chimera_utils_count_option")])

        return task_file

