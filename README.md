# nimble-miner-public

## How to use nimble miner with docker

### 1. Install docker and nvidia-docker
[install-guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
#### Installing with Apt
1. Configure the production repository:
```
$ curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

2. Optionally, configure the repository to use experimental packages:

```
$ sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

3. Update the packages list from the repository:

```
$ sudo apt-get update
```

4. Install the NVIDIA Container Toolkit packages:
```
$ sudo apt-get install -y nvidia-container-toolkit
```
### 2. Config ENV
copy .env.example to .env and edit it
```
cp .env.example .env
```

env example
```
ADDR=nimblexxxx
```
### 3. Start
#### via docker-compose
```
docker-compose up -d
<!-- See Log -->
docker logs -f nimble-miner-public-miner-1
```
#### via docker
```
docker build -t nimble-miner-public:latest .
docker run -d --gpus all --name nimble-miner-public-miner-1 nimble-miner-public:latest "python3 -u /app/execute.py ${YOUR_ADDR}"