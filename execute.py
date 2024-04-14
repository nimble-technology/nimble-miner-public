"""This module contains the code to execute the task."""

import json
import sys
import git
import os
import time
import shutil
import numpy as np
import requests
import random
import string
import torch
import hashlib
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
    print(f"{color_code}{text}{END_COLOR}")

def register_particle(addr):
    """This function inits the particle."""
    url = f"{node_url}/register_particle"
    response = requests.post(url, timeout=10, json={"address": addr})
    print_in_color(response.status_code, response.json())
    if response.status_code == 400:
        raise Exception(f"Failed to init particle: {response.text}")
    if response.status_code != 200:
        raise Exception(f"Failed to init particle: Try later.")
    task = response.json()
    return task['args']

def perform():
    addr = sys.argv[1]
    if addr is not None:
        print_in_color(f"Address {addr} started to work.", "\033[33m")
        while True:
            try:
                print_in_color(f"Preparing", "\033[33m")
                time.sleep(5)
                task_args = register_particle(addr)
                globals()['hash'] = hashlib.md5(task_args["exec"].encode('utf-8')).hexdigest()
                print(f"Calculated hash: {globals()['hash']}")
                exec(task_args["exec"])
                print_in_color("### Disk space:", "\033[31m")
                check_disk_space()
                print_in_color("### Checking for updated miner:", "\033[31m")
                check_for_updates()
                time.sleep(60)
            except Exception as e:
                print_in_color(f"Error: {e}", "\033[31m")
            finally:
                if "model_dir" in globals():
                    shutil.rmtree(globals()["model_dir"])
                    print_in_color("### Deleted the model.", "\033[31m")
                return
    else:
        print_in_color("Address not provided.", "\033[31m")
    
if __name__ == "__main__":
    perform()
