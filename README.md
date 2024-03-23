# Nimble Miner

## Quick Introduction
Nimble is building the first-ever decentralized AI framework.  
Miners execute AI operations and provide computation power to the Network.  
Click on the following link for more information about Nimble and its technology > [https://www.nimble.technology/](https://www.nimble.technology/)

## Installation
This guide will helps you to install the Nimble Miner.

### System Specs Requirements
Recommended:
```
RTX 3080+ GPU
Core i7 13700
16GB RAM
256 GB disk space
```
Minimum
```
RTX 2080+ GPU (Linux/Windows), or M1/M2/M3 Mac chips
Core i5 7400
16GB RAM
256 GB disk space
```

### Install Go
Execute the following commands to install GO.  
Verify the last version [here](https://go.dev/dl/)
```
# Download the GO last version
wget https://go.dev/dl/go1.22.1.linux-amd64.tar.gz

# Delete existing folder and extract the binaries
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz

# Add Go binary path to your system's PATH
export PATH=$PATH:/usr/local/go/bin
```
Verify the Go install and its version.
```
go version
```
It should display the go version

### Install Nimble’s Wallet CLI
Execute the following commands to install the Nimble’s Wallet CLI
```
# Create and go to your nimble folder
mkdir $HOME/nimble && cd $HOME/nimble

# Clone the Nimble's Wallet CLI repository
git clone https://github.com/nimble-technology/wallet-public.git

# Go to the wallet folder
cd wallet-public

# Install
make install
```

### Generate a wallet
```
# Go to the nimble-networkd's folder
cd $HOME/go/bin

# Generate a wallet (replace <wallet_name> by the wallet name you want)
./nimble-networkd keys add <wallet_name>
```
After you've entered your passphrase, your wallet shoud be successfully created and the “address: nimblexxxx” output can confirm that!  
Copy the generated Nimble address and save your wallet information in a safe place.

### Nimble Miner Setup
Note: python3.9 (or above) and pip3 are required for the remaining steps.  
Prepare Python Environment (Linux/Windows Only).
```
# Install venv for Linux
sudo apt update
sudo apt install python3-venv
```
Install the Nimble Miner
```
cd $HOME/nimble
git clone https://github.com/nimble-technology/nimble-miner-public.git
cd nimble-miner-public
make install
```
Activate the nimenv_localminers virtual environment
```
source ./nimenv_localminers/bin/activate
```

### Start Mining
Replace the <wallet_address> by your Nimble wallet address (“nimblexxx”) on the command below.
```
make run addr=<wallet_address>
```

**Congratulations ! You are now mining $NIM !**  

You can stop the miner by pressing CTRL+C   
To resume mining, re-run the command.

## Bonus Tips

### Run the Nimble Miner in background using Screen
Screen is a powerful utility for creating and managing multiple virtual terminal sessions, enabling users to run processes in the background.   
Utilize Screen to run the Nimble Miner while simultaneously maintaining access to your main session.  
Execute the following command to install Screen
```
# Install Screen
sudo apt install screen
```
Create a new Screen session (you can replace “NimbleMinerSession“ with your desired session name)
```
screen -S NimbleMinerSession
```
Start mining on your Screen session
```
make run addr=<wallet_address>
```
**Congratulations ! The Nimble Miner is now running on your Screen Session.**  
Press CTRL+a+d to detach from your Screen session and return to your main session.  
Execute “screen -r“ from your main session if you want to return to your Nimble mining session.
