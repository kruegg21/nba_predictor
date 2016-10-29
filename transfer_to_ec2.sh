#!/bin/bash
INSTANCE=ubuntu@ec2-35-160-200-4.us-west-2.compute.amazonaws.com
DATA=~/Desktop/nba_predictor/data/merged_data.csv
KEY=~/Downloads/EC2_instance1.pem
scp -Ci $KEY $DATA $INSTANCE:~/Desktop/nba_predictor
