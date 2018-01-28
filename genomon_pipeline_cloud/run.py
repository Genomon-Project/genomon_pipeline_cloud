#! /usr/bin/env python

import sys, argparse, tempfile, shutil, os, subprocess, multiprocessing, pkg_resources
from ConfigParser import SafeConfigParser
from batch_engine import *
from sample_conf import Sample_conf

def run(args):

    sample_conf = Sample_conf()
    sample_conf.parse_file(args.sample_conf_file)


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
    from tasks.genomon_expression import *

    star_alignment_task = Star_alignment(args.output_dir, tmp_dir, sample_conf, param_conf)
    fusionfusion_task = Fusionfusion(args.output_dir, tmp_dir, sample_conf, param_conf)
    genomon_expression_task = Genomon_expression(args.output_dir, tmp_dir, sample_conf, param_conf)

    # first stage    
    p1 = multiprocessing.Process(target = batch_engine.execute, args = (star_alignment_task,))
    p1.start()
    p1.join()

    # second stage
    p2 = multiprocessing.Process(target = batch_engine.execute, args = (fusionfusion_task,))
    p3 = multiprocessing.Process(target = batch_engine.execute, args = (genomon_expression_task,))
    p2.start()
    p3.start()

    p2.join()
    p3.join()

    # remove the temporary directory
    # shutil.rmtree(tmp_dir)

