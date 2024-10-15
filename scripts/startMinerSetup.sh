#!/bin/bash
#wget -O link
chmod +x minerSetup.sh
pkill -f ./minerSetup.sh
nohup ./minerSetup.sh ubuntu ec2-54-191-43-123.us-west-2.compute.amazonaws.com ~/.ssh/id_rsa.pub  notebook.nimble.technology &