#!/bin/sh

#source ./$2

export MODEL_PATH=`dirname $PWD`
export SCRIPT_HOME=`dirname $0`
export SCRIPT_PATH=`cd $SCRIPT_HOME; pwd`
export PYTHONPATH=`dirname $SCRIPT_PATH`/lib:$PYTHONPATH
export MODELPATH=`dirname $SCRIPT_PATH`/models
export CONFIGPATH=`dirname $SCRIPT_PATH`/cfg
export TEXTUREPATH=`dirname $SCRIPT_PATH`/images

echo $PYTHONPATH

cd $SCRIPT_PATH
pwd
ppython  ./tw3dr.py $1 $2 $3 $4 $5 $6 $7 $8 $9 
