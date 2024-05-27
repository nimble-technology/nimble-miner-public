"""This module contains the code to execute the task."""

import json
import sys
import git
import os
import time
import shutil
import subprocess
import numpy as np
import requests
import hashlib
import torch
from datetime import datetime
now = datetime.now()
from datasets import load_dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          Trainer, TrainingArguments)


node_url = "https://mainnet.nimble.technology:443"
git_repo_url = "https://github.com/nimble-technology/nimble-miner-public.git"


def check_for_updates():
    """Check for updates in the Git repository."""
    repo = git.Repo(search_parent_directories=True)
    repo.remotes.origin.fetch()
    current_commit = repo.head.commit
    repo.remotes.origin.pull()
    new_commit = repo.head.commit
    if current_commit != new_commit:
        print_in_color("Updated the code. Restarting...", "\033[33m")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    else:
        print_in_color("No updates found. Running latest miner", "\033[33m")


def compute_metrics(eval_pred):
    """This function computes the accuracy of the model."""
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        "accuracy": (predictions == labels).astype(np.float32).mean().item()
    }

# check current disk space
def check_disk_space():
    """This function checks the disk space."""
    total, used, free = shutil.disk_usage("/")
    print_in_color(f"Total: {total / (2**30):.2f} GB", "\033[31m")
    print_in_color(f"Used: {used / (2**30):.2f} GB", "\033[31m")
    print_in_color(f"Free: {free / (2**30):.2f} GB", "\033[31m")

def print_in_color(text, color_code):
    """This function prints the text in the specified color."""
    END_COLOR = "\033[0m"
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color_code}{formatted_now} {text}{END_COLOR}")


def register_particle(addr, gpu_names):
    """This function inits the particle."""
    url = f"{node_url}/register_particle"
    response = requests.post(url, timeout=10, json={"address": addr, "gpu_names": gpu_names})
    print_in_color(response.status_code, "\033[32m")
    if response.status_code == 400:
        raise Exception(f"Failed to init particle: {response.text}")
    if response.status_code != 200:
        raise Exception(f"Failed to init particle: Try later.")
    task = response.json()
    return task['args']


def get_gpu_name():
    try:
        # Run the nvidia-smi command
        result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # Split the result to get each GPU name
        gpu_names = result.stdout.strip().split('\n')
        return gpu_names
    except Exception as e:
        print(f"An error occurred while running nvidia-smi: {e}")
        return []

def perform():
    addr = sys.argv[1]
    if addr is not None:
        print_in_color(f"Address {addr} started to work.", "\033[33m")
        while True:
            try:
                print_in_color("### Checking for updated miner:", "\033[31m")
                check_for_updates()
                print_in_color(f"Preparing", "\033[33m")
                time.sleep(30)
                gpu_names = get_gpu_name()
                task_args = register_particle(addr, gpu_names)
                globals()['hash'] = hashlib.md5(task_args["exec"].encode('utf-8')).hexdigest()
                print(task_args)
                print(f"Calculated hash: {globals()['hash']}")
                exec(task_args["exec"])
                time.sleep(30)
            except Exception as e:
                print_in_color(f"Error: {e}", "\033[31m")
            finally:
                if "model_dir" in globals():
                    shutil.rmtree(globals()["model_dir"])
                    print_in_color("### Deleted the model.", "\033[31m")
                    print_in_color("### Disk space:", "\033[31m")
                    check_disk_space()
                return
    else:
        print_in_color("Address not provided.", "\033[31m")

def log_task(wallet_address, train_runtime, status, file_path='my_logs.json'):
    """
    Logs data to a JSON file, appending a new JSON object for each set of data provided.
    
    :param completed_time: The completion time of an task.
    :param train_runtime: The runtime duration of a training.
    :param file_path: Path to the JSON log file.
    """
    # Create a dictionary to store the data along with a timestamp
    data = {
        "WalletAddr": wallet_address,
        "CompletedTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "TrainRuntime": train_runtime,
        "Status": status
    }
    
    # Try to read the existing data from the file
    try:
        with open(file_path, 'r') as file:
            # Load existing data into a list
            logs = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, start a new list
        logs = []
    
    # Append new data to the list of logs
    logs.append(data)
    
    # Write the updated list back to the file
    with open(file_path, 'w') as file:
        json.dump(logs, file, indent=4)
        
if __name__ == "__main__":
    perform()
