#! /usr/bin/env python

import sys, argparse, tempfile, shutil, os, subprocess, pkg_resources
from ConfigParser import SafeConfigParser


def run(args):

    cparser = SafeConfigParser()
    cparser.read(args.param_conf_file)

    tmp_dir_name = tempfile.mkdtemp()
    print >> sys.stdout, "Creating temporary directory: " +  tmp_dir_name

    sample2seq = {}
    with open(args.sample_conf_file, 'r') as hin:
        for line in hin:
            F = line.rstrip('\n').split(',')
            sample2seq[F[0]] = [F[1], F[2]]


    ##########
    # generate star-alignment-tasks.tsv
    hout = open(tmp_dir_name + "/star-alignment-tasks.tsv", 'w') 
    print >> hout, '\t'.join(["--env SAMPLE", 
                              "--input INPUT1", 
                              "--input INPUT2", 
                              "--output-recursive OUTPUT_DIR",
                              "--input-recursive REFERENCE",
                              "--env STAR_OPTION",
                              "--env SAMTOOLS_SORT_OPTION"])

    for sample in sample2seq:
        print >> hout, '\t'.join([sample, 
                                  sample2seq[sample][0], 
                                  sample2seq[sample][1], 
                                  args.output_dir + "/star/" + sample,
                                  cparser.get("star-alignment", "star_reference"),
                                  cparser.get("star-alignment", "star_option"),
                                  cparser.get("star-alignment", "samtools_sort_option")]) 
    hout.close()
    ############


    ##########
    # generate fusionfusion-tasks.tsv
    hout = open(tmp_dir_name + "/fusionfusion-tasks.tsv", 'w')
    print >> hout, '\t'.join(["--env SAMPLE", 
                              "--input INPUT", 
                              "--output-recursive OUTPUT_DIR",
                              "--input REFERENCE"])
        
    for sample in sample2seq:
        print >> hout, '\t'.join([sample, 
                                  args.output_dir + "/star/" + sample + "/" + sample + ".Chimeric.out.sam", 
                                  args.output_dir + "/fusion/" + sample,
                                  cparser.get("fusionfusion", "reference")]) 
    hout.close()
    ##########


    ##########
    # generate dsub-batch.sh file
    hout = open(tmp_dir_name + "/dsub-batch.sh", 'w')
    print >> hout, "#! /usr/bin/env bash"
    print >> hout, ""

    print >> hout, ' '.join(["dsub", 
                             cparser.get("general", "instance_option"),
                             cparser.get("star-alignment", "resource"),
                             "--logging " + args.output_dir + "/logging",
                             "--image friend1ws/star-alignment",
                             "--tasks " + tmp_dir_name + "/star-alignment-tasks.tsv",
                             "--script " + tmp_dir_name + "/star-alignment-script.sh",
                            "--wait"])

    print >> hout, "" 
    print >> hout, ' '.join(["dsub",
                             cparser.get("general", "instance_option"),
                             cparser.get("fusionfusion", "resource"),
                             "--logging " + args.output_dir + "/logging",
                             "--image friend1ws/fusionfusion",
                             "--tasks " + tmp_dir_name + "/fusionfusion-tasks.tsv",
                             "--script " + tmp_dir_name + "/fusionfusion-script.sh"])
    hout.close()
    ##########


    ##########
    # copy script files
    shutil.copyfile(pkg_resources.resource_filename("genomon_rna_gce", "script/star-alignment-script.sh"), tmp_dir_name + "/star-alignment-script.sh")
    shutil.copyfile(pkg_resources.resource_filename("genomon_rna_gce", "script/fusionfusion-script.sh"), tmp_dir_name + "/fusionfusion-script.sh")
    ##########

        
    ##########
    # execute pipeline
    subprocess.call(["bash", tmp_dir_name + "/dsub-batch.sh"])
    
    # remove the temporary directory
    shutil.rmtree(tmp_dir_name)


