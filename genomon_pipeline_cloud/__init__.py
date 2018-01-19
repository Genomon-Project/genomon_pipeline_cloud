import argparse
from genomon_pipeline_cloud.run import run

def main():

    aparser = argparse.ArgumentParser(prog = "genomon_pipeline_cloud")
    aparser.add_argument("--version", action = "version", version = "genomon_pipeline_cloud-0.1.0a1")
    aparser.add_argument("sample_conf_file", default = None, type = str, help = "Sample config file")
    aparser.add_argument("output_dir", default = None, type = str,
                         help = "Output directory for Google Cloud Storage")
    aparser.add_argument("param_conf_file", help = "Parameter config file", type = str)
    args = aparser.parse_args()

    run(args)

