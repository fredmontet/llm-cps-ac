#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run the previously built Docker image of the heating control chatbot on port 8501.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-09"
__version__ = "1.1"
__email__ = "philippe.marziale@edu.hefr.ch"


import subprocess
import os
from dotenv import load_dotenv


network_name = "optibot-network"
chatbot_name = "heating-chatbot"


# Load environment variables from .env file
load_dotenv()


def check_docker_network(network_name):
    """
    Check if a Docker network exists with the given name.
    """
    result = subprocess.run(
        ["docker", "network", "inspect", network_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def create_docker_network(network_name):
    """
    Create a Docker network (try to remove it before if it already exists).
    """
    if check_docker_network(network_name):
        subprocess.run(["docker", "network", "rm", network_name])
    subprocess.run(["docker", "network", "create", network_name])


def check_docker_container(container_name):
    """
    Check if a Docker container exists with the given name.
    """
    result = subprocess.run(
        ["docker", "inspect", container_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def run_docker_chatbot(chatbot_name, network_name):
    """
    Run the Docker's chatbot image (remove it before if it already exists).
    """
    if check_docker_container(chatbot_name):
        subprocess.run(["docker", "rm", "-f", chatbot_name])

    # Run the chatbot container
    subprocess.run(
        [
            "docker",
            "run",
            "--name",
            chatbot_name,
            "--network",
            network_name,
            "-e",
            f"PORT=8501",
            "-e",
            f"RUNNING_IN_DOCKER=True",
            "-e",
            f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')}",
            "-p",
            "8501:8501",
            chatbot_name + ":latest",
        ]
    )


if __name__ == "__main__":
    create_docker_network(network_name)
    run_docker_chatbot(chatbot_name, network_name)
