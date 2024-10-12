#!/bin/bash
# abort when fail
#set -e
# debug
#set -x

# Function to check if Docker is installed
check_docker_installed() {
  if ! command -v docker &> /dev/null; then
    return 1  # Docker is not installed
  else
    return 0  # Docker is installed
  fi
}

# Function to check if Docker is running
check_docker_running() {
  if ! (docker info > /dev/null 2>&1); then
    return 1  # Docker is not running
  else
    return 0  # Docker is running
  fi
}

# Function to install Docker on macOS
install_docker_mac() {
  echo "Installing Docker on macOS..."
  brew install --cask docker
  echo "Docker installed. Please open Docker Desktop manually."
}

# Function to install Docker on Linux
install_docker_linux() {
  echo "Installing Docker on Linux..."
  sudo apt-get update
  sudo apt-get install -y docker.io
  sudo systemctl enable docker
  echo "Docker installed and started on Linux."
}

change_docker_port() {
    SERVICE_FILE="/lib/systemd/system/docker.service"
    BACKUP_FILE="/lib/systemd/system/docker.service.bak"

    if [ -f "$SERVICE_FILE" ]; then
        echo "Backing up current docker.service file to $BACKUP_FILE"
        sudo cp -n "$SERVICE_FILE" "$BACKUP_FILE"
    else
        echo "docker.service file not found!"
        return 1
    fi

    local port=$1

    NEW_EXECSTART="ExecStart=/usr/bin/dockerd -H fd:// -H tcp://127.0.0.1:$port --containerd=/run/containerd/containerd.sock"

    echo "Modifying ExecStart line in $SERVICE_FILE"
    sudo sed -i 's|ExecStart=.*|'"$NEW_EXECSTART"'|' "$SERVICE_FILE"

    echo "Reloading systemd daemon..."
    sudo systemctl daemon-reload
}

# Function to check if the port is already forwarded
is_port_forwarded() {
    local port=$1
    sudo ps aux | grep "ssh -N -R .*:${port}" | grep -v grep > /dev/null
    return $?
}

# Function to start SSH remote port forwarding
start_ssh_tunnel() {
    local host_port=$1
    echo "Starting SSH port forwarding on port $host_port"

    ssh -N -R "${HUB_HOST}:${host_port}:localhost:${host_port}" "${REMOTE_USER}@${HUB_HOST}" 2>&1 &
    ssh_pid=$!

    sleep 2  # make sure it started
    if ps -p $ssh_pid > /dev/null; then
        echo "SSH port forwarding started successfully on port $host_port"
        return 0
    else
        echo "Error: Remote port forwarding failed on port $host_port"
        return 1
    fi
}

# Function to stop SSH remote port forwarding
stop_ssh_tunnel() {
    local host_port=$1
    echo "Stopping SSH port forwarding for port $host_port"
    local pids=$(sudo ps aux | grep "ssh -N -R .*:${host_port}" | grep -v grep | awk '{print $2}')
    for pid in $pids; do
        kill -9 "$pid" 2>/dev/null
        echo "Killed process $pid, port $host_port has been released"
    done
}

# Function to get running containers by label
get_running_containers() {
    sudo docker ps --filter "label=${LABEL_KEY}=${LABEL_VALUE}" -q
}

# Function to get the host port for a given container ID
get_host_port() {
    local container_id=$1
    sudo docker port "$container_id" "$CONTAINER_PORT" | awk -F: '{print $2}'
}

get_remote_docker_port(){
    echo "Requesting port from remote"

    output=$(docker run --gpus all --runtime=nvidia ubuntu nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits)
    IFS=',' read -r GPU_NAME GPU_MEMORY <<< "$output"
    # get gpu model and memory
    resp=$(curl -s -X POST http://"$HUB_DOMAIN":8000/hub/api/port \
        -H "Content-Type: application/json" \
        -d "{
          \"publicKey\": \"$PUB_KEY\",
          \"machine\": \"$GPU_NAME\",
          \"memory\": \"$GPU_MEMORY\",
          \"port\": \"$DOCKER_PORT\",
          \"ip\": \"$LOCAL_IP\"
        }")
    echo "port resp=$resp"
    NEW_DOCKER_PORT=$(echo "$resp" | jq -r '.port')

    if [ -z "$NEW_DOCKER_PORT" -o "$NEW_DOCKER_PORT" = "null" ] || ! [[ "$NEW_DOCKER_PORT" =~ ^[0-9]+$ ]]; then
        echo "Error: No available port found or the port is not a valid number. Wait to next retry"
        return 0
    fi

    if [ "$DOCKER_PORT" -ne -1 ] && [ "$NEW_DOCKER_PORT" -ne "$DOCKER_PORT" ]; then
        stop_ssh_tunnel "$DOCKER_PORT"
    fi

    if [ "$NEW_DOCKER_PORT" -ne "$DOCKER_PORT" ]; then
        echo "Configuring Docker daemon to listen on TCP port $NEW_DOCKER_PORT..."
        change_docker_port "$NEW_DOCKER_PORT"
        sudo systemctl restart docker
        sudo systemctl status docker |head -n 20
    fi

    DOCKER_PORT="$NEW_DOCKER_PORT"
}

if [ $# -lt 4 ]; then
    echo "Usage: $0 <REMOTE_USER> <HUB_HOST> <HUB_DOMAIN> <PUB_KEY_PATH>"
    exit 1
fi

REMOTE_USER=$1
HUB_HOST=$2
HUB_DOMAIN=$4
PUB_KEY_PATH=$3
PUB_KEY=""
DOCKER_PORT=-1
LOCAL_IP=$(ip addr show | grep "inet " | grep -v 127.0.0.1 |grep -v docker0 | awk '{print $2}' | cut -d/ -f1)

echo "Run the script with sudo."
#read -r -p "
#Please enter the full path of the public key file, and make sure only one pub key in this file: " PUB_KEY_PATH

PUB_KEY_PATH=$(eval echo "$PUB_KEY_PATH")

if [ ! -f "$PUB_KEY_PATH" ]; then
    echo "Error: The specified file does not exist."
    exit 1
fi

pub_key_count=$(grep -v -E '^\s*$|^#' "$PUB_KEY_PATH" | wc -l)

if [ "$pub_key_count" -gt 1 ]; then
    echo "Error: The public key file contains multiple keys."
    exit 1
else
    echo "The public key file is valid and contains only one key."
    PUB_KEY=$(cat "$PUB_KEY_PATH")
    echo "Public key is: $PUB_KEY"
fi

echo "install some lib"
sudo apt-get update;sudo apt-get -y install jq

if check_docker_installed; then
  echo "Docker is already installed."
else
  install_docker_linux
fi

echo "Installing CUDA dependencies..."
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor --yes -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
&& curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

#sudo apt-get update; sudo apt-get install -y nvidia-container-toolkit nvidia-utils-550-server nvidia-driver-550
sudo nvidia-ctk runtime configure --runtime=docker


# Associative array to store container and port mapping
declare -A container_port_map


ssh-keyscan -H "$HUB_HOST" >> ~/.ssh/known_hosts

LABEL_KEY="maintainer"
LABEL_VALUE="nimbleTechnology"
CONTAINER_PORT="8888"
CHECK_INTERVAL=10 # 10 seconds
retries=0
max_retries=50
# Main loop to continuously check for containers and manage port forwarding
while true; do
    if [ $retries -ge $max_retries ]; then
        echo "Docker Port forwarding failed after $max_retries attempts. Need to contract nimble developer"
    fi
    get_remote_docker_port
    if [ "$DOCKER_PORT" -ne -1 ];then

      if is_port_forwarded "$DOCKER_PORT"; then
          echo "DOCKER_PORT=$DOCKER_PORT has been forwarded"
      else
          start_ssh_tunnel "$DOCKER_PORT"
          if [ $? -ne 0 ]; then
              retries=$((retries + 1))
          else
              echo "successfully forwarded ssh port $DOCKER_PORT"
              retries=0
          fi
      fi
    else
      echo "Failed to get docker port, need to wait next retry"
      retries=$((retries + 1))
    fi


    # Get the list of currently running containers
    running_containers=$(get_running_containers)

    # Process each running container
    for container_id in $running_containers; do
        host_port=$(get_host_port "$container_id")
        if [ -z "$host_port" ]; then
            echo "Error: cannot get host port, the Jupyter Notebook does not work properly"
            continue
        fi

        # Check if the port is already forwarded
        if is_port_forwarded "$host_port"; then
            continue
        fi

        echo "Container $container_id, host port $host_port has not been forwarded. Starting remote forward."
        start_ssh_tunnel "$host_port"
        container_port_map["$container_id"]="$host_port"
    done

    # Check for stopped containers and stop their corresponding port forwarding
    for container_id in "${!container_port_map[@]}"; do
        if ! echo "$running_containers" | grep -q "$container_id"; then
            host_port=${container_port_map["$container_id"]}
            echo "Detected stopped container $container_id, stopping corresponding port forwarding for port $host_port."
            stop_ssh_tunnel "$host_port"
            unset container_port_map["$container_id"]
        fi
    done

    sleep $CHECK_INTERVAL
done
