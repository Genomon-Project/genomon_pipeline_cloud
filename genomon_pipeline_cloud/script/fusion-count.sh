#!/bin/bash

set -o errexit
set -o nounset
set -o xtrace

OUTPUT=${OUTPUT_DIR}/${SAMPLE}.Chimeric.count

chimera_utils count ${OPTION} ${INPUT} ${OUTPUT}

