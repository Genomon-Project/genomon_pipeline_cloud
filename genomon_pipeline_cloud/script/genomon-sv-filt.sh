#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace

GenomonSV ${INPUT_BAM} ${OUTPUT_PREFIX} ${PARAM}

