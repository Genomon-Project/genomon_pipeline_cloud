#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace

OUTPUT=${OUTPUT_DIR}/${SAMPLE}.Chimeric.count

mkdir -p ${OUTPUT_DIR}
chimera_utils count ${OPTION} ${INPUT} ${OUTPUT}

