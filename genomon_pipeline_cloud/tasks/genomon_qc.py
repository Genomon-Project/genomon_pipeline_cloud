#! /usr/bin/env python

import pkg_resources
from ..abstract_task import *
 
class Genomon_qc(Abstract_task):

    task_name = "genomon-qc"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Genomon_qc, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
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

            print >> hout, '\t'.join(["--env SAMPLE",
                                      "--input-recursive INPUT_DIR",
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
                                      "--env SAMTOOLS_PARAMS"])

            for sample in sample_conf.qc:
                print >> hout, '\t'.join([sample,
                                          output_dir + "/bam/" + sample,
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
                                          param_conf.get("qc", "samtools_params")])

        return task_file

