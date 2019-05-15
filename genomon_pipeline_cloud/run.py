#! /usr/bin/env python

import sys, os, multiprocessing
   
import genomon_pipeline_cloud.batch_engine as be
import genomon_pipeline_cloud.sample_conf as sc
import genomon_pipeline_cloud.run_conf as rc
import genomon_pipeline_cloud.storage as st

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

        import genomon_pipeline_cloud.tasks.star_alignment as star_alignment
        import genomon_pipeline_cloud.tasks.fusion_count as fusion_count
        import genomon_pipeline_cloud.tasks.fusion_merge as fusion_merge
        import genomon_pipeline_cloud.tasks.fusionfusion as fusionfusion
        import genomon_pipeline_cloud.tasks.genomon_expression as genomon_expression
        import genomon_pipeline_cloud.tasks.intron_retention as intron_retention

        star_alignment_task = star_alignment.Star_alignment(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        fusion_count_task = fusion_count.Fusion_count(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        fusion_merge_task = fusion_merge.Fusion_merge(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        fusionfusion_task = fusionfusion.Fusionfusion(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        genomon_expression_task = genomon_expression.Genomon_expression(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        intron_retention_task = intron_retention.Intron_retention(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        
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
    
        import genomon_pipeline_cloud.tasks.bwa_alignment as bwa_alignment
        import genomon_pipeline_cloud.tasks.sv_parse as sv_parse
        import genomon_pipeline_cloud.tasks.sv_merge as sv_merge
        import genomon_pipeline_cloud.tasks.sv_filt as sv_filt
        import genomon_pipeline_cloud.tasks.mutation_call as mutation_call
        import genomon_pipeline_cloud.tasks.genomon_qc as genomon_qc
        import genomon_pipeline_cloud.tasks.pmsignature as pmsignature
        
        bwa_alignment_task = bwa_alignment.Bwa_alignment(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        p_bwa = multiprocessing.Process(target = batch_engine.execute, args = (bwa_alignment_task,))

        sv_parse_task = sv_parse.SV_parse(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        sv_merge_task = sv_merge.SV_merge(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        sv_filt_task = sv_filt.SV_filt(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        p_sv = multiprocessing.Process(target = batch_engine.seq_execute, args = ([sv_parse_task,sv_merge_task,sv_filt_task],))

        mutation_call_task = mutation_call.Mutation_call(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        pmsignature_task = pmsignature.Pmsignature(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
        p_mutation = multiprocessing.Process(target = batch_engine.seq_execute, args = ([mutation_call_task,pmsignature_task],))

        qc_task = genomon_qc.Genomon_qc(args.output_dir, tmp_dir, sample_conf, param_conf, run_conf)
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
