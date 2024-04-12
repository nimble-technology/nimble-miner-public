# Nimble Miner

## Quick Introduction
Nimble is building the first-ever decentralized AI framework.  
Miners execute AI operations and provide computation power to the Network.  
Click on the following link for more information about Nimble and its technology > [https://www.nimble.technology/](https://www.nimble.technology/)

## System Specifications
These are the system specifications to run the Nimble Miner  
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

## Installation
This guide will helps you to install the Nimble Miner.

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

Note : if you get an error such as "make command not found" please run the following command : 
```
sudo apt-get install make
```

### Generate a wallet
```
# Go to the nimble-networkd's folder
cd $HOME/go/bin

# Generate a wallet (replace <wallet_name> by the wallet name you want)
./nimble-networkd keys add <wallet_name>
```
This will ask you to create a passphrase (password) of your choosing.
After you've entered your passphrase, your wallet shoud be successfully created and the “address: nimblexxxx” output can confirm that!  
Copy the generated Nimble address and save your wallet information in a safe place.

Note : to recover an existing wallet from its mnemonic, please run :
```# Recover a wallet from its mnemonic
./nimble-networkd keys add <wallet_name> --recover
```

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
Replace the <wallet_address> by your Nimble wallet addresses on the command below.
```
make run addr=<wallet_address>
```

Note : if you get an error such as "Failed to find C compiler." please run the following command : 
```
sudo apt-get install build-essential
```

**Congratulations ! You are now mining $NIM !**  

You can stop the miner by pressing CTRL+C   
To resume mining, re-run the command.

## Bonus Tips

### Optimizing your it/s
Depending on your set-up, tweaking the training parameters could lead to better memory utilization and/or an increase of the training speed.
To do so, you need to open the execute.py file and edit the following section : 
```
training_args = TrainingArguments(
        output_dir="my_model", evaluation_strategy="epoch"
    )
```


Please note, some parameters such as fp16 or bf16 may lead to a loss of precision and lower rewards/bad reputation.

A full description can be found here : https://huggingface.co/docs/transformers/en/perf_train_gpu_one



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
