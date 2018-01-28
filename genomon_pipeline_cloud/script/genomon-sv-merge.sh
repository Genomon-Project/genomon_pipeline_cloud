#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace

GenomonSV merge ${CONTROL_INFO} ${MERGE_OUTPUT_FILE} ${PARAM}

