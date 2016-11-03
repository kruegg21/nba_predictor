KEY=~/Downloads/EC2_instance1.pem
PREFIX=ubuntu@ec2-
SUFFIX=.us-west-2.compute.amazonaws.com
IP=35-161-148-176
ssh -i $KEY $PREFIX$1$SUFFIX
