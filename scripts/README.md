# Miner Preparation
## Step 1: Generate Your SSH Public Key on Your GPU Host

### How to Generate an SSH Public Key

Run the ssh-keygen command:
The following command will generate an SSH key pair using the RSA algorithm with a 4096-bit key length:
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
Explanation:

* -t rsa: Specifies the type of key to create (RSA in this case).
* -b 4096: Specifies the key length (4096 bits for enhanced security).
* "your_email@example.com": A comment to help identify the key (typically your email address).

By default, the public key file will be located at /home/your_username/.ssh/id_rsa. If you choose a different location, make sure to remember it as you’ll need it later.
## Step 2: Prepare the Environment on Your GPU Machine
Just copy all these command and paste to your terminal.
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor --yes -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
&& curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update; sudo apt-get install -y nvidia-container-toolkit nvidia-driver-550-server
sudo nvidia-ctk runtime configure --runtime=docker

```
## Step 3: Run the Mining Script
Download the script using the following commands. This script will read your SSH public key from the default location (~/.ssh/id_rsa.pub). If your key is stored in a different location, you can modify the script accordingly.

Once you’ve downloaded the script, ensure the current user has sudo privileges, execute it (without sudo).
```
wget -O minerSetup.sh https://raw.githubusercontent.com/nimble-technology/nimble-miner-public/PROD-2342-miner-readme/scripts/minerSetup.sh 
wget -O startMinerSetup.sh https://raw.githubusercontent.com/nimble-technology/nimble-miner-public/PROD-2342-miner-readme/scripts/startMinerSetup.sh
chmod +x startMinerSetup.sh
./startMinerSetup.sh
```

That’s it! You’re ready to begin mining.

## Step 4: Monitor your miner app
```
# show running containers
docker ps 
# get logs from container
docker logs container_id
```