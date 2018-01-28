#! /usr/bin/env python

import pkg_resources
from ..abstract_task import *
 
class Fusionfusion(Abstract_task):

    task_name = "fusionfusion"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf):
    
        super(Fusionfusion, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            "friend1ws/fusionfusion",
            param_conf.get("fusionfusion", "resource"),
            output_dir + "/logging")
       
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf) 


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf):

        # generate fusionfusion_tasks.tsv
        task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        with open(task_file, 'w') as hout:
            
            print >> hout, '\t'.join(["--env SAMPLE",
                                      "--input INPUT",
                                      "--output-recursive OUTPUT_DIR",
                                      "--input REFERENCE"])
            for sample in sample_conf.fusion:
                print >> hout, '\t'.join([sample[0],
                                          output_dir + "/star/" + sample[0] + "/" + sample[0] + ".Chimeric.out.sam",
                                          output_dir + "/fusion/" + sample[0],
                                          param_conf.get("fusionfusion", "reference")])

        return task_file
