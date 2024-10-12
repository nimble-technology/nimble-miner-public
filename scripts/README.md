# miner prepare
## Step1: upload your gpu machine public key
### how to generate ssh public key
Run the ssh-keygen command:
The following command will generate an SSH key pair using the RSA algorithm with a 4096-bit key length:
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
* -t rsa: Specifies the type of key to create, in this case, RSA.
* 4096: Specifies the key length (4096 bits for better security).
* "your_email@example.com": A comment to help identify the key (typically an email address).

the default location of pub key file is : /home/your_username/.ssh/id_rsa, if you specify other location, please remember it, will use it later.
### upload your key
first login with google, then upload your pub key in http://notebook.nimble.technology:8000/, we will support batch upload later.
## Step2: prepare env in your gpu machine
we will provide a script to set up your env in lots of machine with only one operation later.
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor --yes -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
&& curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update; sudo apt-get install -y nvidia-container-toolkit nvidia-driver-550-server
sudo nvidia-ctk runtime configure --runtime=docker

```
## Step3: Run a script to begin mining 
download script from this link, the default location of your pub key file is : ~/.ssh/id_rsa.pub, you can replace it if you want.
Then run it with sudo, then nimble server can access your gpu, that 's all.



