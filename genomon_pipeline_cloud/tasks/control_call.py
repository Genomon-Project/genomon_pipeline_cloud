#! /usr/bin/env python

import os
import abstract_task
 
class Control_call(abstract_task.Abstract_task):

    task_name = "control-call"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Control_call, self).__init__(
            "%s/script/%s.sh" % (os.path.dirname(__file__), self.__class__.task_name),
            param_conf.get("control_call", "image"),
            param_conf.get("control_call", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            hout.write('\t'.join(["--env SAMPLE",
                                  "--input-recursive INPUT_DIR",
                                  "--output-recursive OUTPUT_DIR",
                                  "--env META",
                                  "--input-recursive REFERENCE",
                                  "--env FISHER_SINGLE_OPTION",
                                  "--env FISHER_SINGLE_SAMTOOLS"]) 
                                  + "\n")

            control_panel_li = []
            for tumo_sample, normal_sample, panel_name  in sample_conf.mutation_call:
                if panel_name != None: control_panel_li.append(panel_name)
            control_panel_li_uniq = list(set(control_panel_li))
           
            control_sample_li = [] 
            for panel_name in sample_conf.control_panel:
                if panel_name in control_panel_li_uniq: control_sample_li.extend(sample_conf.control_panel[panel_name])
            control_sample_li_uniq = list(set(control_sample_li))

            for sample in control_sample_li_uniq:
                hout.write('\t'.join([sample,
                                      output_dir + "/bam/" + sample,
                                      output_dir + "/mutation/control_panel/" + sample,
                                      run_conf.get_meta_info(param_conf.get("control_call", "image")),
                                      param_conf.get("control_call", "reference"),
                                      param_conf.get("control_call", "fisher_single_option"),
                                      param_conf.get("control_call", "fisher_single_samtools")]) 
                                      + "\n")

        return task_file

