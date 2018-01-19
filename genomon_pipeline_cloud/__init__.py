import argparse
from genomon_rna_gce.run import run

def main():

    aparser = argparse.ArgumentParser(prog = "genomon_rna_gce")
    aparser.add_argument("--version", action = "version", version = "genomon_rna_gce-0.2.0")
    aparser.add_argument("sample_conf_file", default = None, type = str, help = "Sample config file")
    aparser.add_argument("output_dir", default = None, type = str,
                         help = "Output directory for Google Cloud Storage")
    aparser.add_argument("param_conf_file", help = "Parameter config file", type = str)
    args = aparser.parse_args()

    run(args)

