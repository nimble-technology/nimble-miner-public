"""This module contains the code to execute the task."""

import json
import sys
import git
import os
import time
import shutil
import numpy as np
import torch
from datasets import load_dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          Trainer, TrainingArguments)
import httpx


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
  

def execute(task_args):
    """This function executes the task."""
    print_in_color("Starting training...", "\033[34m")  # Blue for start

    tokenizer = AutoTokenizer.from_pretrained(task_args["model_name"])

    def tokenize_function(examples):
        return tokenizer(
            examples["text"], padding="max_length", truncation=True
        )
  
    model = AutoModelForSequenceClassification.from_pretrained(
        task_args["model_name"], num_labels=task_args["num_labels"]
    )
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    dataset = load_dataset(task_args["dataset_name"])
    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    small_train_dataset = (
        tokenized_datasets["train"].shuffle(seed=task_args["seed"]).select(range(task_args["num_rows"]))
    )
    small_eval_dataset = (
        tokenized_datasets["train"].shuffle(seed=task_args["seed"]).select(range(task_args["num_rows"]))
    )
    training_args = TrainingArguments(
        output_dir="my_model", evaluation_strategy="epoch", save_strategy='epoch',
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model("my_model")


def print_in_color(text, color_code):
    """This function prints the text in the specified color."""
    END_COLOR = "\033[0m"
    print(f"{color_code}{text}{END_COLOR}")


def register_particle(addr):
    """This function inits the particle."""
    url = f"{node_url}/register_particle"
    data = {"address": addr}

    try:
        # Create an HTTP/2 client instance
        with httpx.Client(http2=True) as client:

            # Make the POST request
            response = client.post(url, json=data, timeout=10)

            # Ensure it's successful
            response.raise_for_status()

            # Return the response JSON
            task = response.json()
            return task['args']

    except httpx.HTTPStatusError as exc:
        raise Exception(f"Failed to init particle: Try later.") from exc


def complete_task(wallet_address):
    """This function completes the task."""

    url = f"{node_url}/complete_task"
    files = {
        "file1": open("my_model/config.json", "rb"),
        "file2": open("my_model/training_args.bin", "rb"),
        "file3": open("my_model/model.safetensors", "rb"),
    }
    json_data = json.dumps({"address": wallet_address})
    files["r"] = (None, json_data, "application/json")

    try:
        # Create an HTTP/2 client instance
        with httpx.Client(http2=True) as client:

            # Make the POST request
            response = client.post(url, files=files, timeout=60)

            # Ensure it's successful
            response.raise_for_status()

            # Convert the response content to JSON
            result = response.json()

    except httpx.HTTPStatusError as exc:
        raise Exception(f"Failed to complete task: Try later.") from exc

    return result


def perform():
    addr = sys.argv[1] 
    if addr is not None:
        print_in_color(f"Address {addr} started to work.", "\033[33m")
        while True:
            try:
                print_in_color(f"Preparing", "\033[33m")
                time.sleep(5)
                task_args = register_particle(addr)
                print_in_color(f"Address {addr} received the task.", "\033[33m")
                execute(task_args)
                print_in_color(f"Address {addr} executed the task.", "\033[32m")
                complete_task(addr)
                print_in_color(f"Address {addr} completed the task. Waiting for next", "\033[32m")
                shutil.rmtree("my_model")
                print_in_color("### Deleted the model.", "\033[31m")
                print_in_color("### Disk space:", "\033[31m")
                check_disk_space()
                print_in_color("### Checking for updated miner:", "\033[31m")
                check_for_updates()
                time.sleep(60)
            except Exception as e:
                print_in_color(f"Error: {e}", "\033[31m")
    else:
        print_in_color("Address not provided.", "\033[31m")


if __name__ == "__main__":
    perform()
