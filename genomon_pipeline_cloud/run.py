#! /usr/bin/env python

import sys, argparse, tempfile, shutil, os, subprocess, pkg_resources
from ConfigParser import SafeConfigParser


def run(args):

    sample_conf = {}
    with open(args.sample_conf_file, 'r') as hin:
        for line in hin:
            F = line.rstrip('\n').split(',')
            sample_conf[F[0]] = [F[1], F[2]]

    param_conf = SafeConfigParser()
    param_conf.read(args.param_conf_file)


    # tmp_dir = tempfile.mkdtemp()
    # temporary procedure
    tmp_dir = os.getcwd() + "/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        print >> sys.stdout, "Creating temporary directory: " +  tmp_dir


    ##########
    # RNA
    from tasks.star_alignment import *
    from tasks.fusionfusion import *    

    star_alignment_task = Star_alignment(args.output_dir, tmp_dir, sample_conf, param_conf)
    fusionfusion_task = Fusionfusion(args.output_dir, tmp_dir, sample_conf, param_conf)
    
    print
    print star_alignment_task
    print
    print fusionfusion_task
    """
    ##########
    # generate dsub-batch.sh file
    hout = open(tmp_dir_name + "/dsub-batch.sh", 'w')
    print >> hout, "#! /usr/bin/env bash"
    print >> hout, ""

    print >> hout, ' '.join(["dsub", 
                             param_conf.get("general", "instance_option"),
                             param_conf.get("star-alignment", "resource"),
                             "--logging " + args.output_dir + "/logging",
                             "--image friend1ws/star-alignment",
                             "--tasks " + tmp_dir_name + "/star-alignment-tasks.tsv",
                             "--script " + tmp_dir_name + "/star-alignment-script.sh",
                            "--wait"])

    print >> hout, "" 
    print >> hout, ' '.join(["dsub",
                             param_conf.get("general", "instance_option"),
                             param_conf.get("fusionfusion", "resource"),
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
    """

