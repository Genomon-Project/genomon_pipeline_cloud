[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# genomon_pipeline_cloud

# Installation

```sh
git clone https://github.com/Genomon-Project/genomon_pipeline_cloud.git
cd genomon_pipeline_cloud
pip install . --upgrade
```

# Quick Start

```sh
genomon_pipeline_cloud \
  example_conf/sample_dna.csv \
  s3://{your_bucket}/genomon_pipeline_cloud_test \
  example_conf/param_dna_awsub.cfg
```

see detail https://github.com/Genomon-Project/genomon_pipeline_cloud/wiki
