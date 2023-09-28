#!/bin/bash

{$SPARK_HOME}/bin/spark-submit \
  --master spark://DESKTOP-RRS69N2.:7077 \
  ./pySpark_transform_load_rds.py --grand_prix=$1 --gp_index=$2
