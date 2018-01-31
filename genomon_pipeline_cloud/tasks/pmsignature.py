#! /usr/bin/env python

import pkg_resources
from ..abstract_task import *
 
class Pmsignature(Abstract_task):

    task_name = "pmsignature"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf):

        super(Pmsignature, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            "genomon/pmsignature",
            param_conf.get("pmsignature", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf):

        task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        with open(task_file, 'w') as hout:

            print >> hout, '\t'.join(["--input-recursive INPUT_DIR",
                                      "--output-recursive OUTPUT_DIR",
                                      "--env MODE",
                                      "--env BGFLAG",
                                      "--env BS_GENOME",
                                      "--env SIG_MIN",
                                      "--env SIG_MAX",
                                      "--env TRDIRFLAG",
                                      "--env TRIALNUM",
                                      "--env TXDB_TRANSCRIPT"])

            if param_conf.getboolean("pmsignature", "enable"):
                print >> hout, '\t'.join([output_dir + "/mutation/",
                                          output_dir + "/pmsignature_test/sample",
                                          "ind",
                                          param_conf.get("pmsignature", "bgflag"),
                                          param_conf.get("pmsignature", "bs_genome"),
                                          param_conf.get("pmsignature", "signum_min"),
                                          param_conf.get("pmsignature", "signum_max"),
                                          param_conf.get("pmsignature", "trdirflag"),
                                          param_conf.get("pmsignature", "trialnum"),
                                          param_conf.get("pmsignature", "txdb_transcript")])

            if param_conf.getboolean("signature", "enable"):
                print >> hout, '\t'.join([output_dir + "/mutation/",
                                          output_dir + "/signature_test/sample",
                                          "full",
                                          param_conf.get("signature", "bgflag"),
                                          param_conf.get("signature", "bs_genome"),
                                          param_conf.get("signature", "signum_min"),
                                          param_conf.get("signature", "signum_max"),
                                          param_conf.get("signature", "trdirflag"),
                                          param_conf.get("signature", "trialnum"),
                                          param_conf.get("signature", "txdb_transcript")])
        return task_file

