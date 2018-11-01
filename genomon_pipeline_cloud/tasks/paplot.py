#! /usr/bin/env python

import os
import pkg_resources
from ..abstract_task import *
 
class Paplot(Abstract_task):

    task_name = "paplot"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Paplot, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            param_conf.get("paplot", "image"),
            param_conf.get("paplot", "resource"),
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
        
        def to_oneliner_signature(tag, output_dir, sig_min, sig_max):
            
            header = []
            data = []
            counter = 0
            for sig in range(sig_min, sig_max+1):
                counter += 1
                header.append("--input INPUT_" + tag.upper() + str(counter))
                data.append("%s/pmsignature.%s.result.%d.json" % (output_dir, tag, sig))
            
            return ["\t".join(header), "\t".join(data)]
            
        def to_oneliner_starqc(tag, stage, bam_files, output_suffix):
            
            header = []
            data = []
            counter = 0
            for sample in stage:
                counter += 1
                header.append("--input INPUT_" + tag.upper() + str(counter))
                if type(sample) == type(()):
                    sample = sample[0]
                bam = bam_files[sample]
                bam_dir = os.path.dirname(bam)
                data.append("%s/%s%s" % (bam_dir, sample, output_suffix))
            
            return ["\t".join(header), "\t".join(data)]
        
        items = {"star": ["", ""], "fusion": ["", ""], "qc": ["", ""], "sv": ["", ""], "mutation": ["", ""], "signature": ["", ""], "pmsignature": ["", ""]}

        if run_conf.analysis_type == "rna":
            items["star"]     = to_oneliner_starqc("starqc", sample_conf.qc, sample_conf.bam_file, ".Log.final.out")
            items["fusion"]   = to_oneliner("fusion", sample_conf.fusion, output_dir + "/fusion", ".genomonFusion.result.filt.txt")

        elif run_conf.analysis_type == "dna":
            items["qc"]       = to_oneliner("qc", sample_conf.qc, output_dir + "/qc", ".genomonQC.result.txt")
            items["sv"]       = to_oneliner("sv", sample_conf.sv_detection, output_dir + "/sv", ".genomonSV.result.filt.txt")
            # items["mutation"] = to_oneliner("mutation", sample_conf.mutation_call, output_dir + "/mutation", ".genomon_mutation.result.filt.txt")
            items["signature"]  = to_oneliner_signature("full", output_dir + "/pmsignature/" + run_conf.sample_conf_name, param_conf.getint("signature", "signum_min"), param_conf.getint("signature", "signum_max"))
            items["pmsignature"]= to_oneliner_signature("ind", output_dir + "/pmsignature/" + run_conf.sample_conf_name, param_conf.getint("pmsignature", "signum_min"), param_conf.getint("pmsignature", "signum_max"))
        
        header = []
        data = []
        for key in sorted(items.keys()):
            if len(items[key][0]) == 0:
                continue
            header.append(items[key][0])
            data.append(items[key][1])
        
        #task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            print >> hout, '\t'.join(['\t'.join(header),
                                      "--input CONFIG_FILE",
                                      "--output-recursive OUTPUT_DIR",
                                      "--env REMARKS",
                                      "--env TITLE"])

            if param_conf.getboolean("paplot", "enable"):
                remarks = param_conf.get("paplot", "remarks")
                remarks += "<ul><li>%s</li>" % (run_conf.pipeline_version)
                for soft in sorted(param_conf.get("paplot", "software").split(",")):
                    remarks += "<li>" + param_conf.get(soft, "image") + "</li>"
                remarks += "</ul>"
                
                print >> hout, '\t'.join(['\t'.join(data),
                                          param_conf.get("paplot", "config_file"),
                                          output_dir + "/paplot/" + run_conf.sample_conf_name,
                                          remarks,
                                          param_conf.get("paplot", "title")])

        return task_file

