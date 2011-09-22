#!/bin/sh

#source ./$2
export vendor_nets
export local_nets
export private_nets
export remote_nets
export security_zones
export MODEL_PATH=`dirname $PWD`

export SCRIPT_HOME=`dirname $0`
export SCRIPT_PATH=`cd $SCRIPT_HOME; pwd`
export PYTHONPATH=`dirname $SCRIPT_PATH`/lib;$PYTHONPATH
export MODELPATH=`dirname $SCRIPT_PATH`/models
export CONFIGPATH=`dirname $SCRIPT_PATH`/cfg
export TEXTUREPATH=`dirname $SCRIPT_PATH`/images
export XMLPATH=`dirname $SCRIPT_PATH`/xml
echo $PYTHONPATH
echo $XMLPATH

cd $SCRIPT_PATH
pwd
ppython  ./viewgibson.py $1 $2 $3 $4
