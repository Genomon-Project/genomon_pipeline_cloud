#! /usr/bin/env python

import sys, os, multiprocessing
   
import batch_engine as be
import sample_conf as sc
import run_conf as rc
import storage as st

if sys.version_info.major == 2:
    import ConfigParser as cp
else:
    import configparser as cp

def run(args):
    args.output_dir = args.output_dir.rstrip("/")
    
    sample_conf = sc.Sample_conf()
    sample_conf.parse_file(args.sample_conf_file, args.output_dir, args.analysis_type)
    
    param_conf = cp.ConfigParser()
    param_conf.read(args.param_conf_file)

    run_conf = rc.Run_conf(sample_conf_file = args.sample_conf_file, 
                        param_conf_file = args.param_conf_file,
                        analysis_type = args.analysis_type,
                        output_dir = args.output_dir)
                        
    # tmp_dir = tempfile.mkdtemp()
    # temporary procedure
    tmp_dir = os.getcwd() + "/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        print ("Creating temporary directory: " +  tmp_dir)

    log_dir = os.getcwd() + "/log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print ("Creating log directory: " +  log_dir)
        
    # preparing batch job engine
    if args.engine == "dsub":
        factory = be.Dsub_factory()
    elif args.engine == "azmon":
        factory = be.Azmon_factory()
    elif args.engine == "ecsub":
        factory = be.Ecsub_factory()
        factory.s3_wdir = args.output_dir + "/ecsub"
        factory.wdir = tmp_dir + "/ecsub"
    else:
        factory = be.Awsub_factory()

    factory.dryrun = args.dryrun
    batch_engine = be.Batch_engine(factory, param_conf.get("general", "instance_option"))
    
    # upload config files
    storage = st.Storage(dryrun = args.dryrun)
    storage.upload(args.sample_conf_file, run_conf.sample_conf_storage_path, create_bucket = True)
    storage.upload(args.param_conf_file, run_conf.param_conf_storage_path, create_bucket = True)
    
    ##########
    # RNA
    if args.analysis_type == "rna":

        import tasks.star_alignment
        import tasks.fusion_count
        import tasks.fusion_merge
        import tasks.fusionfusion
        import tasks.genomon_expression
        import tasks.intron_retention

        star_alignment_task = tasks.star_alignment.Star_alignment(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        fusion_count_task = tasks.fusion_count.Fusion_count(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        fusion_merge_task = tasks.fusion_merge.Fusion_merge(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        fusionfusion_task = tasks.fusionfusion.Fusionfusion(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        genomon_expression_task = tasks.genomon_expression.Genomon_expression(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        intron_retention_task = tasks.intron_retention.Intron_retention(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        
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
    
        import tasks.bwa_alignment
        import tasks.sv_parse
        import tasks.sv_merge
        import tasks.sv_filt
        import tasks.mutation_call
        import tasks.genomon_qc
        import tasks.pmsignature
        
        bwa_alignment_task = tasks.bwa_alignment.Bwa_alignment(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        p_bwa = multiprocessing.Process(target = batch_engine.execute, args = (bwa_alignment_task,))

        sv_parse_task = tasks.sv_parse.SV_parse(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        sv_merge_task = tasks.sv_merge.SV_merge(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        sv_filt_task = tasks.sv_filt.SV_filt(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        p_sv = multiprocessing.Process(target = batch_engine.seq_execute, args = ([sv_parse_task,sv_merge_task,sv_filt_task],))

        mutation_call_task = tasks.mutation_call.Mutation_call(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        pmsignature_task = tasks.pmsignature.Pmsignature(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        p_mutation = multiprocessing.Process(target = batch_engine.seq_execute, args = ([mutation_call_task,pmsignature_task],))

        qc_task = tasks.genomon_qc.Genomon_qc(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
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

if __name__ == "__main__":

    import argparse
    
    aparser = argparse.ArgumentParser(prog = "genomon_pipeline_cloud")
    aparser.add_argument("--version", action = "version", version = "genomon_pipeline_cloud-0.0.0")
    aparser.add_argument("--output_dir", type = str, default = "./test")
    aparser.add_argument("--engine", choices = ["awsub", "dsub", "azmon", "ecsub"], type = str, default = "ecsub")
    aparser.add_argument("--dryrun", action = 'store_true')
    aparser.add_argument('analysis_type', choices=['dna', 'rna'])
    aparser.add_argument("sample_conf_file", type = str)
    aparser.add_argument("param_conf_file", type = str)
    
    class C:
        pass
    
    dna = C()
    aparser.parse_args(args=['dna', 
                             os.path.dirname(__file__) + "/../example_conf/sample_dna.csv",
                             os.path.dirname(__file__) + "/../example_conf/param_dna_ecsub.cfg",
                             "--dryrun"], 
                        namespace = dna)
    run(dna)
    
    
    rna = C()
    aparser.parse_args(args=['rna', 
                             os.path.dirname(__file__) + "/../example_conf/sample_rna.csv",
                             os.path.dirname(__file__) + "/../example_conf/param_rna_ecsub.cfg",
                             "--dryrun"], 
                        namespace = rna)
    run(rna)
    