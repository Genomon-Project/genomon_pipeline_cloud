#! /usr/bin/env python

import sys, os, multiprocessing
from ConfigParser import SafeConfigParser
from batch_engine import Batch_engine, Dsub_factory, Azmon_factory, Ecsub_factory, Awsub_factory
from sample_conf import Sample_conf
from run_conf import Run_conf
from storage import Storage

def run(args):
    args.output_dir = args.output_dir.rstrip("/")
    
    sample_conf = Sample_conf()
    sample_conf.parse_file(args.sample_conf_file, args.output_dir, args.analysis_type)
    
    param_conf = SafeConfigParser()
    param_conf.read(args.param_conf_file)

    run_conf = Run_conf(sample_conf_file = args.sample_conf_file, 
                        param_conf_file = args.param_conf_file,
                        analysis_type = args.analysis_type,
                        output_dir = args.output_dir)
                        
    # tmp_dir = tempfile.mkdtemp()
    # temporary procedure
    tmp_dir = os.getcwd() + "/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        print >> sys.stdout, "Creating temporary directory: " +  tmp_dir

    log_dir = os.getcwd() + "/log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print >> sys.stdout, "Creating log directory: " +  log_dir
        
    # preparing batch job engine
    if args.engine == "dsub":
        factory = Dsub_factory()
    elif args.engine == "azmon":
        factory = Azmon_factory()
    elif args.engine == "ecsub":
        factory = Ecsub_factory()
        factory.s3_wdir = args.output_dir + "/ecsub"
        factory.wdir = "/tmp/ecsub"
    else:
        factory = Awsub_factory()

    factory.dryrun = args.dryrun
    batch_engine = Batch_engine(factory, param_conf.get("general", "instance_option"))
    
    # upload config files
    storage = Storage(dryrun = args.dryrun)
    storage.upload(args.sample_conf_file, run_conf.sample_conf_storage_path, create_bucket = True)
    storage.upload(args.param_conf_file, run_conf.param_conf_storage_path, create_bucket = True)
    
    ##########
    # RNA
    if args.analysis_type == "rna":

        from tasks.star_alignment import Star_alignment
        from tasks.fusion_count import Fusion_count   
        from tasks.fusion_merge import Fusion_merge 
        from tasks.fusionfusion import Fusionfusion    
        from tasks.genomon_expression import Genomon_expression
        from tasks.intron_retention import Intron_retention

        star_alignment_task = Star_alignment(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        fusion_count_task = Fusion_count(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        fusion_merge_task = Fusion_merge(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        fusionfusion_task = Fusionfusion(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        genomon_expression_task = Genomon_expression(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        intron_retention_task = Intron_retention(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        
        p_star = multiprocessing.Process(target = batch_engine.execute, args = (star_alignment_task,))
        p_star.start()
        p_star.join()

        p_fusion = multiprocessing.Process(target = batch_engine.seq_execute, args = ([fusion_count_task, fusion_merge_task, fusionfusion_task],))
        p_expression = multiprocessing.Process(target = batch_engine.execute, args = (genomon_expression_task,))
        p_ir = multiprocessing.Process(target = batch_engine.execute, args = (intron_retention_task,))

        p_fusion.start()
        p_expression.start()
        p_ir.start()

        p_fusion.join()
        p_expression.join()
        p_ir.join()
        

    ##########
    # DNA
    elif args.analysis_type == "dna":
    
        from tasks.bwa_alignment import Bwa_alignment
        from tasks.sv_parse import SV_parse
        from tasks.sv_merge import SV_merge
        from tasks.sv_filt import SV_filt
        #from tasks.control_call import Control_call
        #from tasks.control_merge import Control_merge
        from tasks.mutation_call import Mutation_call
        from tasks.genomon_qc import Genomon_qc
        from tasks.pmsignature import Pmsignature
        
        bwa_alignment_task = Bwa_alignment(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        p_bwa = multiprocessing.Process(target = batch_engine.execute, args = (bwa_alignment_task,))

        sv_parse_task = SV_parse(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        sv_merge_task = SV_merge(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        sv_filt_task = SV_filt(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        p_sv = multiprocessing.Process(target = batch_engine.seq_execute, args = ([sv_parse_task,sv_merge_task,sv_filt_task],))

        #control_call_task = Control_call(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        #control_merge_task = Control_merge(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        mutation_call_task = Mutation_call(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        pmsignature_task = Pmsignature(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        # p_mutation = multiprocessing.Process(target = batch_engine.seq_execute, args = ([control_call_task,control_merge_task,mutation_call_task,pmsignature_task],))
        p_mutation = multiprocessing.Process(target = batch_engine.seq_execute, args = ([mutation_call_task,pmsignature_task],))

        qc_task = Genomon_qc(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        p_qc = multiprocessing.Process(target = batch_engine.execute, args = (qc_task,))
        
        p_bwa.start()
        p_bwa.join()
        
        p_sv.start()
        p_mutation.start()
        p_qc.start()

        p_sv.join()
        p_mutation.join()
        p_qc.join()
        
    
    # paplot stage
    from tasks.paplot import Paplot
    paplot_task = Paplot(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
    
    p_paplot = multiprocessing.Process(target = batch_engine.execute, args = (paplot_task,))
    p_paplot.start()
    p_paplot.join()
    
    if args.engine == "ecsub":
        factory.print_summary(run_conf, log_dir)
