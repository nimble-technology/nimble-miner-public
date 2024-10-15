#!/bin/bash
#wget -O link
chmod +x minerSetup.sh
pkill -f ./minerSetup.sh
nohup ./minerSetup.sh ubuntu ~/.ssh/id_rsa.pub  notebook.nimble.technology &