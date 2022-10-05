#! /usr/bin/env python

import os
import genomon_pipeline_cloud.abstract_task as abstract_task
 
class Fusionfusion(abstract_task.Abstract_task):

    task_name = "fusionfusion"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):
    
        super(Fusionfusion, self).__init__(
            self.__class__.task_name,
            param_conf.get("fusionfusion", "image"),
            param_conf.get("fusionfusion", "resource"),
            output_dir + "/logging")
       
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf) 


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        # generate fusionfusion_tasks.tsv
        #task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:
            
            hout.write('\t'.join(["--env SAMPLE",
                                  "--input-recursive INPUT_DIR",
                                  "--output-recursive OUTPUT_DIR",
                                  "--env OPTION",
                                  "--env FILT_OPTION",
                                  "--input REFERENCE",
                                  "--input-recursive MERGED_COUNT_DIR",
                                  "--env PANEL_NAME"]) 
                                  + "\n")

            for sample, panel_name  in sample_conf.fusion:

                bam = sample_conf.bam_file[sample]
                bam_dir = os.path.dirname(bam)

                record = [sample,
                          bam_dir,
                          output_dir + "/fusion/" + sample,
                          param_conf.get("fusionfusion", "fusionfusion_option"),
                          param_conf.get("fusionfusion", "filt_option"),
                          param_conf.get("fusionfusion", "reference")]

                if panel_name != None:
                     record.append(output_dir + "/fusion/control_panel/" + panel_name)
                     record.append(panel_name)
                else:
                     record.append("")
                     record.append("")

                hout.write('\t'.join(record) + "\n")

        return task_file
