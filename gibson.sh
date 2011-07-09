#!/bin/sh

source ./$2
export vendor_nets
export local_nets
export private_nets
export remote_nets
export security_zones
ppython main.py $1
