[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# genomon_rna_gce

This is a software to perform cancer transcriptome sequence analysis using Google Compute Engine.
More specifically: 
* Execute alignment of fastq files (assuming these are set up at Google Cloud Storage) using [STAR](https://github.com/alexdobin/STAR).
* Identify fusion transcripts using our inhouse software ([fusionfusion](https://github.com/Genomon-Project/fusionfusion)).
* Key result files (BAM files and fusion transcripts) are put in Google Cloud Storage.

This software heavily rely on a great batch job engine software, [dsub](https://github.com/googlegenomics/dsub).

# Installation

```sh
git clone git@github.com:friend1ws/genomon_rna_gce.git
cd genomon_rna_gce
pip install . --upgrade
```

# Prerequisites

Since this software heavily rely on the dsub software,
You need to set up for dsub.

1. Sign up for a Google Cloud Platform accout and create your project.
1. Enable the APIs.
1. Install the Google Cloud SDK.
1. And `GOOGLE_APPLICATION_CREDENTIALS` on your machine and JSON file representing the credentials, which is created by `gcloud application-default login` (See [here](https://developers.google.com/identity/protocols/application-default-credentials) for more information).
1. Create a Google Cloud Storage bucket.

See **Getting started on Google Cloud** section in the README.md file in the dsub repository.

# Quick Start

## Basic Commands
```
genomon_rna_gce [-h] [--version] sample_conf_file output_dir param_conf_file
```

We need three arguments

## Sample Cofiguration file

This is the CSV format file, in which the 1st column is the sample name (which can be set arbitrarily), and the 2nd and 3rd columns are the pathes for the 1st and 2nd fastq format sequence data. We have prepared several sequence data for execution tests,
which you can access [here](https://console.cloud.google.com/storage/browser/genomon_rna_gce/sequence_data/).

For the sample configuration files for these test data, see the [example_conf/sample-conf.csv](https://github.com/friend1ws/genomon_rna_gce/blob/master/example_conf/sample-conf.csv) file for example.

We have prepared several sequence 

## Output directory

Set the path of output directory (Google Cloud Storage).

## Parameter Configuration file

This is the configuration file of parameters used in the workflow.
You can use the [example_conf/param.cfg](https://github.com/friend1ws/genomon_rna_gce/blob/master/example_conf/param.cfg) with just modifying **general** section.

```
[general]
instance_option = --project [your_project] --zones [your_favorite_zone]
```

## Test

```
genomon_rna_gce example_conf/sample-conf.tsv gs://[your_gcs_bucket]/[specified_output_dir_name] example_conf/param.cfg
```

# Result

## BAM file

You will be able to find the BAM file at ``gs://[your_gcs_bucket]/[specified_output_dir_name]/star/[sample_name]/``.

### Fusion Transcripts

The list of fusion transcripts can be found at ``gs://[your_gcs_bucket]/[specified_output_dir_name]/fusion/[sample_name]/``.
See also [fusionfusion](https://github.com/Genomon-Project/fusionfusion) repository.


