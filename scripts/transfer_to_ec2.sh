#!/bin/bash
IP=35-161-120-71
IP2=35-163-19-4
PREFIX=ubuntu@ec2-
SUFFIX=.us-west-2.compute.amazonaws.com
INSTANCE=ubuntu@ec2-35-160-200-4.us-west-2.compute.amazonaws.com
DATA=~/Desktop/nba_predictor/data/merged_data.csv
KEY=~/Downloads/EC2_instance1.pem
scp -rCi $KEY $DATA $PREFIX$1$SUFFIX:~/Desktop/nba_predictor/data
