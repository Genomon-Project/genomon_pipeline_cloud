#! /usr/bin/env python

import os
import genomon_pipeline_cloud.abstract_task as abstract_task
 
class Fusion_count(abstract_task.Abstract_task):

    task_name = "fusion-count"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Fusion_count, self).__init__(
            self.__class__.task_name,
            param_conf.get("fusion_count_control", "image"),
            param_conf.get("fusion_count_control", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            hout.write('\t'.join(["--env SAMPLE",
                                  "--input INPUT",
                                  "--output-recursive OUTPUT_DIR",
                                  "--env META",
                                  "--env OPTION"]) 
                                  + "\n")

            control_panel_li = []
            for tumor_sample, panel_name  in sample_conf.fusion:
                if panel_name != None: control_panel_li.append(panel_name)
            control_panel_li_uniq = list(set(control_panel_li))
           
            control_sample_li = [] 
            for panel_name in sample_conf.control_panel:
                if panel_name in control_panel_li_uniq: control_sample_li.extend(sample_conf.control_panel[panel_name])
            control_sample_li_uniq = list(set(control_sample_li))

            for sample in control_sample_li_uniq:

                bam = sample_conf.star_bam_file[sample]
                bam_dir = os.path.dirname(bam)

                hout.write('\t'.join([sample,
                                      bam_dir + "/" + sample + ".Chimeric.out.sam",
                                      output_dir + "/fusion/control_panel/" + sample,
                                      run_conf.get_meta_info(param_conf.get("fusion_count_control", "image")),
                                      param_conf.get("fusion_count_control", "chimera_utils_count_option")]) 
                                      + "\n")

        return task_file

