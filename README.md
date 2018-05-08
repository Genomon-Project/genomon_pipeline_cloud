[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# genomon_pipeline_cloud

# Installation

```sh
git clone https://github.com/Genomon-Project/genomon_pipeline_cloud.git
cd genomon_pipeline_cloud
python setup.py build install
```

# External Prerequisites:

Install one of the following batch job engines:

 - [awsub](https://github.com/otiai10/awsub/r)
 - [ecsub (AWS only)](https://github.com/aokad/ecsub)
 - azuremon (Micosoft Azure only)


# Quick Start

```sh
genomon_pipeline_cloud dna \
  example_conf/sample_dna.csv \
  s3://{your_bucket}/genomon_pipeline_cloud_test \
  example_conf/param_dna_awsub.cfg
```

see detail :notebook: https://github.com/Genomon-Project/genomon_pipeline_cloud/wiki
