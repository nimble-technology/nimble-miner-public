"""This module contains the code to execute the task."""

import json
import sys
import time
import numpy as np
import requests
import torch
from requests import HTTPError
from datasets import load_dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          Trainer, TrainingArguments)
from loguru import logger

NODE_URL = "https://mainnet.nimble.technology:443"
MODEL = "google-bert/bert-base-uncased"


logger.add("output.log")


logger.info(f"Initializing at {NODE_URL}\nUsing address: {sys.argv[1]}")

def compute_metrics(eval_pred):
    logger.info("Computing metrics")
    """This function computes the accuracy of the model."""
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        "accuracy": (predictions == labels).astype(np.float32).mean().item()
    }


@logger.catch()
def execute(task_args):
    """This function executes the task."""
    logger.info("Executing task")
    
    print_in_color("Starting training...", "\033[34m")  # Blue for start

    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    def tokenize_function(examples):
        logger.info("Tokenizing task")
        return tokenizer(
            examples["text"], padding="max_length", truncation=True
        )

    try: 

        model = AutoModelForSequenceClassification.from_pretrained(
            task_args["model_name"], num_labels=task_args["num_labels"]
        )
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

    except Exception as error:
        logger.error(f"Error during loading of the model {error}")
        raise Exception(f"Error during loading of the model")
    
    logger.info(f"Model loaded on {device}" )

    dataset = load_dataset(task_args["dataset_name"])
    logger.debug(dataset)
    logger.info(f"Dataset {task_args['dataset_name']} loaded")
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    logger.info("Dataset tokenized")

    logger.info("Tokenizing training run")
    logger.info(f"""
{task_args["seed"]}
{task_args["num_rows"]}
""")
    
    if not tokenized_datasets:
        raise ValueError("Datasets not loaded correctly!")

    try:
        small_train_dataset = (
            tokenized_datasets["training"].shuffle(seed=task_args["seed"]).select(range(task_args["num_rows"]))
        )
        logger.info("Tokenization complete")
        logger.info("Tokenizing evaluating run")
        small_eval_dataset = (
            tokenized_datasets["test"].shuffle(seed=task_args["seed"]).select(range(task_args["num_rows"]))
        )
    except Exception as error:
        raise Exception(f"Error during tokenizing: {error}")
    
    logger.error(f"Error during tokenization {error}")
    logger.info("Tokenizing complete")
    
    
    training_args = TrainingArguments(
        output_dir="my_model", evaluation_strategy="epoch"
    )

    if not small_eval_dataset or small_train_dataset:
        raise ValueError("Datasets not loaded correctly!")
    
    logger.info("Results will be saved to ./my_model")
    logger.info("Starting training run")
    
    try:
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=small_train_dataset,
            eval_dataset=small_eval_dataset,
            compute_metrics=compute_metrics,
        )
    except Exception as error:
        logger.error(f"Error during training{error}")
        raise Exception(f"Error during training{error}")
    
    logger.info("Starting training run")
    trainer.train()
    logger.info("Training run complete")
    trainer.save_model("my_model")
    logger.info("Model has been saved to ./my_model")


def print_in_color(text, color_code):
    """This function prints the text in the specified color."""
    END_COLOR = "\033[0m"
    print(f"{color_code}{text}{END_COLOR}")


def register_particle(addr):
    """This function inits the particle."""

    logger.info("Registering particle")
    url = f"{NODE_URL}/register_particle"
    
    try:
        response = requests.post(url, timeout=10, json={"address": addr})
        if response.status_code == 200:
            task = response.json()
            return task['args']
    except HTTPError as error:
        logger.error(f"Error during http request:\n{response.content}")
        raise HTTPError(f"Error during http request:\n{error}\nResponse:{response.content}")


def complete_task(wallet_address):
    """This function completes the task."""
    logger.info("Final step")

    url = f"{NODE_URL}/complete_task"
    json_data = json.dumps({"address": wallet_address})
    files = {
        "file1": open("my_model/config.json", "rb"),
        "file2": open("my_model/training_args.bin", "rb"),
        "r": (None, json_data, "application/json")
    }

    logger.info("making request")
    
    try:
        response = requests.post(url, files=files, timeout=60)
        if response.status_code == 200:
            logger.info("Complete!")
            return response.json()
    
    except HTTPError as error:
        logger.error(f"Error during http request:\n{response.content}")
        raise HTTPError(f"Error during http request:\n{error}\nResponse:{response.content}")


def perform():
    logger.info("Performing Task")
    
    addr = sys.argv[1] 

    if addr is not None:
        print_in_color(f"Address {addr} started to work.", "\033[33m")
        while True:
            try:
                print_in_color(f"Preparing", "\033[33m")
                time.sleep(10)
                task_args = register_particle(addr)
                print_in_color(f"Address {addr} received the task.", "\033[33m")
                execute(task_args)
                print_in_color(f"Address {addr} executed the task.", "\033[32m")
                complete_task(addr)
                print_in_color(f"Address {addr} completed the task. ", "\033[32m")
            except Exception as e:
                print_in_color(f"Error: {e}", "\033[31m")
    else:
        print_in_color("Address not provided.", "\033[31m")
    
if __name__ == "__main__":
    perform()
