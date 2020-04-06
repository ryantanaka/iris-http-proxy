#!/bin/bash

set -e

export TOP_DIR=`pwd`

export WORK_DIR=$HOME/workflows
if ls /local-scratch/ >/dev/null 2>&1; then
    export WORK_DIR=/local-scratch/$USER/workflows
fi
mkdir -p $WORK_DIR

export RUN_ID=test-workflow-`date +'%s'`

# create the catalogs from the templates
mkdir -p generated
envsubst < $TOP_DIR/sites.xml.template > $TOP_DIR/sites.xml

# generate the workflow
#./workflow_gen.py

# plan and submit the  workflow
pegasus-plan \
    --conf pegasus.conf \
    --force \
    --dir $WORK_DIR \
    --relative-dir $RUN_ID \
    --sites condorpool \
    --staging-site condorpool=origin \
    --output-site local \
    --dax workflow.xml \
    --cluster horizontal \
    --submit
