# Nimble Miner Setup Guide
Welcome to the Nimble Miner setup guide. This document is designed to help you get started with the Nimble Miner, a tool forked from https://github.com/nimble-technology/nimble-miner-public to show your logs for how many successful tasks you've completed. I've structured this guide to make the setup process as intuitive as possible.

# Introduction
The Nimble Miner allows users to contribute to the Nimble Network by performing AI inference tasks in exchange for rewards. This guide will take you through the necessary steps to set up your mining operations.

For curious readers to learn more about how to get started please read here first: https://discord.com/channels/1139328143400894604/1165053157391478825/1225876548255744121

# System Specifications
``` RTX 3080+ GPU
Core i7 13700
16GB RAM
20 GB disk space 
```

# Installation
This guide will use pm2 to handle the session to run multiple GPUs, 2x4090, 4x3090... that can be rented here: [VAST](https://cloud.vast.ai/?ref_id=120915)

# Rent GPUs
This guide works well with the **Cuda:12.0.1-Devel-Ubuntu22.04** template:
![image](https://github.com/b5prolh/nimble-miner-public/assets/18376326/b1e13f1b-3c6d-46f8-8862-95676717841a)

If this is the first time you've used vast and dont know how to connect, please watch this short instructional video: https://www.youtube.com/watch?v=KraLVgFS4vU

# Install
Copy these commands and paste them into the terminal. Make sure u select the correct template **Cuda:12.0.1-Devel-Ubuntu22.04**. If not, you should copy and paste the following code, line by line.

```
apt-get update -y && apt-get upgrade -y && apt install build-essential

curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs && sudo npm install pm2 -g 

sudo rm -rf /usr/local/go
curl https://dl.google.com/go/go1.22.1.linux-amd64.tar.gz | sudo tar -C/usr/local -zxvf - ;
cat <<'EOF' >>$HOME/.bashrc
export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export GO111MODULE=on
export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin
EOF
source $HOME/.bashrc

cd
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
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
After you've entered your passphrase, your wallet will be created and the output “address: nimblexxxx” is confirmation it was successful.
Copy the generated Nimble Address and save your wallet information in a safe place.

# Recover your wallet
If you already have a seed phrase for your wallet, u can recover it by running the following commands:
```
cd && cd $HOME/nimble && cd wallet-public
./nimble-networkd keys add YOUR_WALLET_NAME --recover
```

After you've entered your seedphrase and passphrase, your wallet will be created and the output “address: nimblexxxx” is confirmation it was successful.

# Run miner
## 1xGPUs
Run miner: ```pm2 start "CUDA_VISIBLE_DEVICES=0 make run addr=YOUR_SUBWALLET_1" --name nimble ```
See log: ``` pm2 logs nimble```
## 2xGPUs
Run miner with GPU1: ```pm2 start "CUDA_VISIBLE_DEVICES=0 make run addr=YOUR_SUBWALLET_1" --name nimble_1```
See log: ``` pm2 logs nimble_1 ```

Run miner with GPU2: ```pm2 start "CUDA_VISIBLE_DEVICES=1 make run addr=YOUR_SUBWALLET_1" --name nimble_2 ```
See log: ``` pm2 logs nimble_2 ```

If u want to see the logs of all of the sessions, please use: 
``` 
pm2 logs
```

You can run the same commands that you ran above, for 4xGPus, 8xGPUs and so on, just remember to change the **CUDA_VISIBLE_DEVICES** number.

# Show logs
Run the command below to show the tasks that completed or failed. This log will be saved to **my_logs.json** in your local storage. You should back it up when u destroy your instance, if not it will be lost.
``` 
make logs
```

![image](https://github.com/b5prolh/nimble-miner-public/assets/18376326/f93ff3b5-f69e-45cd-8553-404519e70f74)


# Some additional commands for pm2
using CTRL + C to close your log session and continue using your terminal.

## Start a new session
```
pm2 start "Your_Command" --name YOUR_SESSION_NAME
```

## See logs
``` 
pm2 logs YOUR_SESSION_NAME
```

## List session
``` 
pm2 list
```

# Contact
you can contact me if have any issues related to this guide
Discord: mytt0918
[Telegram](https://t.me/OxCaos)
[Twitter](https://twitter.com/kiwigamefi)


# Donate
If you would like to buy me starbucks, consider doing so by making a small domation to one of the addresses below:

TRC20 
``` 
TQe1d7nZq3E3T3b6FsU5E5VeapNGVBeB18
 ```
BEP20 
``` 
0xf96bbf1532287fb309409dbc4e6491eae46c030a
 ```
Sol 
```
7ixWCfwk3xVoYkr2utfCkdqG3cVcUTJQ8cZJmpioGH5g 
```

Many thanks and I hope we will all become rich and prosperous from mining these precious NIM tokens!
