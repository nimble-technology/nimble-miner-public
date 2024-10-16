#!/bin/bash
wget -O minerSetup.sh https://raw.githubusercontent.com/nimble-technology/nimble-miner-public/main/scripts/minerSetup.sh
chmod +x minerSetup.sh
pkill -f ./minerSetup.sh
nohup ./minerSetup.sh ubuntu ~/.ssh/id_rsa.pub  notebook.nimble.technology &