#! /usr/bin/env python

import pkg_resources
from ..abstract_task import *
 
class Mutation_call(Abstract_task):

    task_name = "mutation-call"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf):

        super(Mutation_call, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            "genomon/mutation_call",
            param_conf.get("mutation_call", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf):

        task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        with open(task_file, 'w') as hout:

            print >> hout, '\t'.join(["--env SAMPLE1",
                                      "--env SAMPLE2",
                                      "--env CONTROL_BAM_LIST",
                                      "--input-recursive INPUT_DIR1",
                                      "--input-recursive INPUT_DIR2",
                                      "--output-recursive OUTPUT_DIR",
                                      "--input-recursive REFERENCE",
                                      "--input-recursive HOTSPOT_DB",
                                      "--input-recursive ANNOTATION_DB",
                                      "--env FISHER_SINGLE_OPTION",
                                      "--env FISHER_PAIR_OPTION",
                                      "--env HOTSPOT_OPTION",
                                      "--env REALIGNMENT_OPTION",
                                      "--env INDEL_OPTION",
                                      "--env BREAKPOINT_OPTION",
                                      "--env FILTER_PAIR_OPTION",
                                      "--env FILTER_SINGLE_OPTION",
                                      "--env ACTIVE_HGVD_2016_FLAG",
                                      "--env ACTIVE_EXAC_FLAG"])

            for sample in sample_conf.mutation_call:
                sample2 = sample[1] if sample[1] != None else "None"
                sample2bam = output_dir+"/bam/"+sample[1] if sample[1] != None else ""
                control_panel = sample[2] if sample[2] != None else "None"
                print >> hout, '\t'.join([sample[0],
                                          sample2,
                                          control_panel,
                                          output_dir + "/bam/" + sample[0],
                                          sample2bam,
                                          output_dir + "/mutation/" + sample[0],
                                          param_conf.get("mutation_call", "reference"),
                                          param_conf.get("mutation_call", "hotspot_database"),
                                          param_conf.get("mutation_call", "annotation_database"),
                                          param_conf.get("mutation_call", "fisher_single_option"),
                                          param_conf.get("mutation_call", "fisher_pair_option"),
                                          param_conf.get("mutation_call", "hotspot_call_option"),
                                          param_conf.get("mutation_call", "realignment_option"),
                                          param_conf.get("mutation_call", "indel_option"),
                                          param_conf.get("mutation_call", "breakpoint_option"),
                                          param_conf.get("mutation_call", "filter_pair_option"),
                                          param_conf.get("mutation_call", "filter_single_option"),
                                          param_conf.get("mutation_call", "active_hgvd_2016_flag"),
                                          param_conf.get("mutation_call", "active_exac_flag")])

        return task_file

