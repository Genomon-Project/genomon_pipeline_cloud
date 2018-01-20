[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# genomon_pipeline_cloud

# Installation

```sh
git clone git@github.com:friend1ws/genomon_pipeline_cloud.git
cd genomon_pipeline_cloud
pip install . --upgrade
```

# Quick Start

```sh
genomon_pipeline_cloud \
  example_conf/sample_awsub.csv \
  s3://awsub-test-friend1ws/genomon_pipeline_cloud_test \
  example_conf/param_awsub.cfg
```
