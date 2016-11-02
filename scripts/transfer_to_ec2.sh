#!/bin/bash
IP=35-161-120-71
IP2=172-31-20-190
PREFIX=ubuntu@ec2-
SUFFIX=.us-west-2.compute.amazonaws.com
INSTANCE=ubuntu@ec2-35-160-200-4.us-west-2.compute.amazonaws.com
DATA=~/Desktop/nba_predictor/data/merged_data.csv
KEY=~/Downloads/EC2_instance1.pem
scp -Ci $KEY $DATA $PREFIX$IP2$SUFFIX:~/Desktop/nba_predictor
