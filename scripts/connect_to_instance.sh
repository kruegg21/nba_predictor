KEY=~/Downloads/EC2_instance1.pem
PREFIX=ubuntu@ec2-
SUFFIX=.us-west-2.compute.amazonaws.com
IP=35-160-76-32
ssh -i $KEY $PREFIX$IP$SUFFIX
