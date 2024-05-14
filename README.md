# Nimble Miner Setup Guide
Welcome to the Nimble Miner setup guide. This document is designed to help you get started with the Nimble Miner, a tool that fork from https://github.com/nimble-technology/nimble-miner-public to show your task complete logs. I've structured this guide to make the setup process as straightforward as possible.

# Introduction
Nimble Miner allows users to contribute to the Nimble network by performing AI inference tasks in exchange for rewards. This guide will take you through the necessary steps to set up your mining operation.

For curious readers to learn more about how to start please read it first https://discord.com/channels/1139328143400894604/1165053157391478825/1225876548255744121

# System Specifications
``` RTX 3080+ GPU
Core i7 13700
16GB RAM
20 GB disk space 
```

# Installation
This guideline will use pm2 to handle session to run with multiple GPUs like 2x4090, 4x3090... that rent on [VAST](https://cloud.vast.ai/?ref_id=120915)

# Rent GPUs
This guidline working good with **Cuda:12.0.1-Devel-Ubuntu22.04** template for only one times to copy and paste
![image](https://github.com/b5prolh/nimble-miner-public/assets/18376326/b1e13f1b-3c6d-46f8-8862-95676717841a)

If this is first time you use vast and dont know how to connect, please see it first: https://www.youtube.com/watch?v=KraLVgFS4vU

# Install
Just coppy all these command and past to your terminal. Make sure u select correct template **Cuda:12.0.1-Devel-Ubuntu22.04**. If not, should copy line by line

```
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs && sudo npm install pm2 -g 

cd
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash /miniconda3/miniconda.sh -b -u -p /miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
source $HOME/.bashrc

sudo rm -rf /usr/local/go
curl https://dl.google.com/go/go1.22.1.linux-amd64.tar.gz | sudo tar -C/usr/local -zxvf - ;
cat <<'EOF' >>$HOME/.bashrc
export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export GO111MODULE=on
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin
EOF
source $HOME/.bashrc

sudo apt update -y && sudo apt install build-essential

source $HOME/.bashrc
conda create -n nimble python=3.11 -y
conda activate nimble

mkdir $HOME/nimble && cd $HOME/nimble

git clone https://github.com/nimble-technology/wallet-public.git

cd wallet-public

make install

cd  $HOME/nimble
git clone https://github.com/b5prolh/nimble-miner-public.git
cd nimble-miner-public
make install
source ./nimenv_localminers/bin/activate
```
# Generate a wallet
``` 
cd && cd $HOME/nimble && cd wallet-public

./nimble-networkd keys add YOUR_WALLET_NAME

```
After you've entered your passphrase, your wallet shoud be successfully created and the “address: nimblexxxx” output can confirm that!
Copy the generated Nimble address and save your wallet information in a safe place.

# Run miner
## 1xGPUs
Run miner: ```pm2 start "CUDA_VISIBLE_DEVICES=0 make run addr=YOUR_SUBWALLET_1" --name nimble ```
See log: ``` pm2 logs nimble```
## 2xGPUs
Run miner with first gpu: ```pm2 start "CUDA_VISIBLE_DEVICES=0 make run addr=YOUR_SUBWALLET_1" --name nimble_1```
See log: ``` pm2 logs nimble_1 ```

Run miner with second gpu: ```pm2 start "CUDA_VISIBLE_DEVICES=1 make run addr=YOUR_SUBWALLET_1" --name nimble_2 ```
See log: ``` pm2 logs nimble_2 ```

Run Same for 4xGPus, 8xGPUs, just remember change **CUDA_VISIBLE_DEVICES** number

# Show logs
``` make logs ```
![image](https://github.com/b5prolh/nimble-miner-public/assets/18376326/f93ff3b5-f69e-45cd-8553-404519e70f74)


# Some command for pm2
using CTRL + C to close logs session to continue using your terminal

## Start new session
```pm2 start "Your_Command" --name YOUR_SESSION_NAME ```

## See logs
``` pm2 logs YOUR_SESSION_NAME ```

## See list session
``` pm2 list ```

# Contact
you can contact me if have any 
