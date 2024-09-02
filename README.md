# Nimble Miner Setup Guide
Welcome to the Nimble Miner setup guide. This document is designed to help you get started with the **NEW** Nimble Miner. New mining tasks are optimized to reduce GPU computing cost to 95%. This guide makes the setup process as easy as possible.

# Introduction
Nimble Miner allows users to contribute to the Nimble network by performing AI training and inferencing tasks in exchange for rewards. This guide will take you through the necessary steps to set up your mining operation.


# System Specifications
``` 
Linux OS
Nvidia GPU with Cuda
4GB RAM
1 GB disk space 
GNU LIBC >= 2.34
```

# Rent GPUs
This guidline working good with **Cuda:12.0.1-Devel-Ubuntu22.04** template for only one times to copy and paste
![image](https://github.com/b5prolh/nimble-miner-public/assets/18376326/b1e13f1b-3c6d-46f8-8862-95676717841a)

If this is first time you use vast and dont know how to connect, please see it first: https://www.youtube.com/watch?v=KraLVgFS4vU

# Install
## Install Nvidia Driver and Cuda

Select the proper version for your Nvidia GPUs drivers and install like following

```
sudo add-apt-repository ppa:graphics-drivers/ppa 
sudo apt update 
sudo apt install nvidia-driver-550-server
sudo apt install nvidia-cuda-toolkit
```

## Install Curl

```
sudo apt install curl
sudo apt-get install -y libcurl4-openssl-dev
```

# Generate a wallet
``` 
cd && cd $HOME/nimble && cd wallet-public
./nimble-networkd keys add YOUR_WALLET_NAME --recover

```
After you've entered your passphrase, your wallet shoud be successfully created and the “address: nimblexxxx” output can confirm that! Copy the generated Nimble address and save your wallet information in a safe place.

# Recover a wallet
If you already have seed pharse of wallet, u can recover it by command
```
cd && cd $HOME/nimble && cd wallet-public
./nimble-networkd keys add YOUR_WALLET_NAME --recover
```

After you've entered your seed pharse and pass pharse, you wallet should be successfully create and the “address: nimblexxxx” output can confirm that!

# Set Wallet

Put your nimble address in **/etc/nimbleservice/nimbleservice.conf** file in following format. Make sure you have read permission for this file.
```
NIMBLE_PUBKEY=nimble17haajcrvtnkcu85h8l9qvdxs9vzc63mvlen4qt
```

# Run miner

Run miner:


```
git clone git@github.com:nimble-technology/nimble-miner-public.git
cd nimble-miner-public
chmod +x nimbleminer
./nimbleminer
```
Logs will be printed on console
```
NIMBLE_PUBKEY=nimble17haajcrvtnkcu85h8l9qvdxs9vzc63mvlen4qt

Nimble Miner Service Output:
GPU 0: Tesla M60 (UUID: GPU-ac3583f3-6ead-2168-43bd-61d3a55a4dfa)
GPU 1: Tesla M60 (UUID: GPU-63864136-feb7-6eb3-ac43-9dade00c1f77)
nimble17haajcrvtnkcu85h8l9qvdxs9vzc63mvlen4qt
Try to get task...
Got one task...
Finish 1 percent of task ...
Finish 2 percent of task ...
Finish 3 percent of task ...
Finish 4 percent of task ...
Finish 5 percent of task ...
```



# Contact
You can contact us if have any issue related this guideline
[Discord](https://discord.gg/KjSC8eKE)
[Twitter](https://x.com/Nimble_Network)

