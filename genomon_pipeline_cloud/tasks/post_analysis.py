#! /usr/bin/env python

import os
import abstract_task
 
class PostAnalysis(abstract_task.Abstract_task):

    task_name = "post_analysis"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf, mode):

        super(PostAnalysis, self).__init__(
            "%s/script/%s.sh" % (os.path.dirname(__file__), self.__class__.task_name),
            param_conf.get("post_analysis", "image"),
            param_conf.get("post_analysis", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf, mode)

    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf, mode):
        
        def pairs_to_case(pairs):
            samples = {
                "case1": [],
                "case2": [],
                "case3": [],
                "case4": []
            }
            for sample in pairs:
            
                if type(sample) != type(()):
                    break
                    
                if len(sample) == 3:
                    if sample[1] == None:
                        if sample[2] == None:
                            samples["case4"].append(sample[0])
                        else:
                            samples["case3"].append(sample[0])
                    else:
                        if sample[2] == None:
                            samples["case2"].append(sample[0])
                        else:
                            samples["case1"].append(sample[0])
                
                elif len(sample) == 2:
                    if sample[1] == None:
                        samples["case2"].append(sample[0])
                    else:
                        samples["case1"].append(sample[0])
            
            return samples
        
        def get_boolean(conf, section, option):
            if not section in conf.sections(): return True
            if not option in conf.options(section): return True
            return conf.getboolean(section, option)
            
        def minimam_param(param_conf, mode, section):
            
            raw_flgs = {
                "case1": True,
                "case2": True,
                "case3": True,
                "case4": True,
            }
            filt_flgs = {
                "case1": True,
                "case2": True,
                "case3": True,
                "case4": True,
            }
            if mode == "fusion":
                raw_flgs["case3"] = False
                raw_flgs["case4"] = False
                filt_flgs["case3"] = False
                filt_flgs["case4"] = False
            
            for i in range(1,5):
                if get_boolean(param_conf, section, "output_raw_all") == False:
                    raw_flgs["case%d" % i] = get_boolean(param_conf, section, "output_raw_case%d" % i)
                if get_boolean(param_conf, section, "output_filt_all") == False:
                    filt_flgs["case%d" % i] = get_boolean(param_conf, section, "output_filt_case%d" % i)
            
            return [raw_flgs, filt_flgs]
            
        def to_oneliner(samples, output_dir, suffix):
            
            data = []
            for sample in samples:
                data.append("%s/%s/%s%s" % (output_dir, sample, sample, suffix))
            
            return data
            
        stage_conf = {
            "star": {
                "output_dir": output_dir + "/star",
                "suffix": ".Log.final.out",
            },
            "fusion": {
                "pairs": sample_conf.fusion,
                "output_dir": output_dir + "/fusion",
                "suffix": ".genomonFusion.result.txt",
                "suffix_filt": ".genomonFusion.result.filt.txt",
                "section": "merge_format_fusionfusion",
            },
            "qc": {
                "output_dir": output_dir + "/qc",
                "suffix": ".genomonQC.result.txt",
            },
            "sv": {
                "pairs": sample_conf.sv_detection,
                "output_dir": output_dir + "/sv",
                "suffix": ".genomonSV.result.txt",
                "suffix_filt": ".genomonSV.result.filt.txt",
                "section": "merge_format_sv"
            },
            "mutation": {
                "pairs": sample_conf.mutation_call,
                "output_dir": output_dir + "/mutation",
                "suffix": ".genomon_mutation.result.txt",
                "suffix_filt": ".genomon_mutation.result.filt.txt",
                "section": "merge_format_mutation"
            }
        }
        
        data = []
        option = []
        if mode == "qc" or mode == "star":
            data = to_oneliner(sample_conf.qc, stage_conf[mode]["output_dir"], stage_conf[mode]["suffix"])
        else:
            cases = pairs_to_case(stage_conf[mode]["pairs"])
            [raw_flgs, filt_flgs] = minimam_param(param_conf, mode, stage_conf[mode]["section"])

            for key in sorted(raw_flgs.keys()):
                if raw_flgs[key]:
                    data.extend(to_oneliner(cases[key], stage_conf[mode]["output_dir"], stage_conf[mode]["suffix"]))
                if filt_flgs[key]:
                    data.extend(to_oneliner(cases[key], stage_conf[mode]["output_dir"], stage_conf[mode]["suffix_filt"]))
            
            for op in sorted(param_conf.options(stage_conf[mode]["section"])):
                option.append("--%s:%s %s" % (stage_conf[mode]["section"], op, param_conf.get(stage_conf[mode]["section"], op)))
                
        header = []
        for i in range(len(data)):
            header.append("--input INPUT" + str(i))
        
        #task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            hout.write('\t'.join(["\t".join(header),
                                      "--input SAMPLE_SHEET",
                                      "--input CONFIG_FILE",
                                      "--output-recursive OUTPUT_DIR",
                                      "--env MODE",
                                      "--env ADD_OPTION"]) + "\n")
            """
            import pprint
            pprint.pprint (header)
            pprint.pprint (data)
            pprint.pprint (option)
            """
            if param_conf.getboolean("post_analysis", "enable") and len(data) > 0:
                hout.write('\t'.join(["\t".join(data),
                                      "s3://hgc-aokad/output_dna/dna.csv",
                                      "s3://hgc-aokad/conf/genomon_post_analysis.cfg",
                                      output_dir + "/post_analysis/" + run_conf.sample_conf_name,
                                      mode,
                                      " ".join(option)])
                                      + "\n")

        return task_file

