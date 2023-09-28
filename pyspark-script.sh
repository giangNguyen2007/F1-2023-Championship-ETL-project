#!/bin/bash

~/spark/spark-3.2.4-bin-hadoop3.2/bin/spark-submit \
  --master spark://DESKTOP-RRS69N2.:7077 \
  /root/projects/gng-pyspark-1/gng-pyspark-forSubmission03.py --grand_prix=$1 --gp_index=$2