#! /usr/bin/env python

import sys, argparse, tempfile, shutil, os, subprocess, pkg_resources
from ConfigParser import SafeConfigParser
from batch_engine import *

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

    # preparing batch job engine
    if args.engine == "dsub":
        factory = Dsub_factory()
    else:
        factory = Awsub_factory()

    batch_engine = Batch_engine(factory, param_conf.get("general", "instance_option"))

    ##########
    # RNA
    from tasks.star_alignment import *
    from tasks.fusionfusion import *    

    star_alignment_task = Star_alignment(args.output_dir, tmp_dir, sample_conf, param_conf)
    fusionfusion_task = Fusionfusion(args.output_dir, tmp_dir, sample_conf, param_conf)

    batch_engine.execute(star_alignment_task)
    batch_engine.execute(fusionfusion_task)  

    """
    # remove the temporary directory
    shutil.rmtree(tmp_dir_name)
    """

