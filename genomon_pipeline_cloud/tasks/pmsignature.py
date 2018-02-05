#! /usr/bin/env python

import pkg_resources
from ..abstract_task import *

class Pmsignature(Abstract_task):

    task_name = "pmsignature"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Pmsignature, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            param_conf.get("pmsignature", "image"),
            param_conf.get("pmsignature", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        def to_oneliner(tag, stage, output_dir, output_suffix):
            
            header = []
            data = []
            counter = 0
            for sample in stage:
                counter += 1
                header.append("--input INPUT_" + tag.upper() + str(counter))
                if type(sample) == type(()):
                    sample = sample[0]
                data.append("%s/%s/%s%s" % (output_dir, sample, sample, output_suffix))
            
            return ["\t".join(header), "\t".join(data)]
            
        [header, data] = to_oneliner("mutation", sample_conf.mutation_call, output_dir + "/mutation", ".genomon_mutation.result.filt.txt")
        
        #task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        task_file = "{}/{}-tasks-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            print >> hout, '\t'.join([header,
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
                print >> hout, '\t'.join([data,
                                          output_dir + "/pmsignature/" + run_conf.sample_conf_name,
                                          "ind",
                                          param_conf.get("pmsignature", "bgflag"),
                                          param_conf.get("pmsignature", "bs_genome"),
                                          param_conf.get("pmsignature", "signum_min"),
                                          param_conf.get("pmsignature", "signum_max"),
                                          param_conf.get("pmsignature", "trdirflag"),
                                          param_conf.get("pmsignature", "trialnum"),
                                          param_conf.get("pmsignature", "txdb_transcript")])

            if param_conf.getboolean("signature", "enable"):
                print >> hout, '\t'.join([data,
                                          output_dir + "/pmsignature/" + run_conf.sample_conf_name,
                                          "full",
                                          param_conf.get("signature", "bgflag"),
                                          param_conf.get("signature", "bs_genome"),
                                          param_conf.get("signature", "signum_min"),
                                          param_conf.get("signature", "signum_max"),
                                          param_conf.get("signature", "trdirflag"),
                                          param_conf.get("signature", "trialnum"),
                                          param_conf.get("signature", "txdb_transcript")])
        return task_file
