#! /usr/bin/env python

import pkg_resources

 
class Star_alignment(Abstract_task):

    task_name = "star_alignment"

    def __init__(self, sample_conf, param_conf):
    
        super(Star_alignment, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "data/script/{}.sh".format(self.__class__.task_name)),
            "friend1ws/star_alignment",
            get_resource_param("star_alignment"),
            param_conf.log_dir)
        
        self.task_file = task_file_generation(sample_conf)


    def task_file_generation(self, dir_name, sample_conf, param_conf):

        # generate star-alignment-tasks.tsv
        with open("{}/{}_tasks.tsv".format(dir_name, task_name), 'w') as hout:

            print >> hout, '\t'.join(["--env SAMPLE",
                                      "--input INPUT1",
                                      "--input INPUT2",
                                      "--output-recursive OUTPUT_DIR",
                                      "--input-recursive REFERENCE",
                                      "--env STAR_OPTION",
                                      "--env SAMTOOLS_SORT_OPTION"])

            for sample in sample_conf:
                print >> hout, '\t'.join([sample,
                                          sample2seq[sample][0],
                                          sample2seq[sample][1],
                                          args.output_dir + "/star/" + sample,
                                          cparser.get("star-alignment", "star_reference"),
                                          cparser.get("star-alignment", "star_option"),
                                          cparser.get("star-alignment", "samtools_sort_option")])


