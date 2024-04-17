#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run the heating chatbot and boiler simulator simultaneously in Docker containers.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-09"
__version__ = "1.0"
__email__ = "philippe.marziale@edu.hefr.ch"


import threading

from chatbot.docker.build import build_docker_chatbot
from chatbot.docker.run import run_docker_chatbot
from chatbot.docker.run import create_docker_network
from simulator.docker.build import build_docker_simulator
from simulator.docker.run import run_docker_simulator


# Docker network and container names
network_name = "optibot-network"
chatbot_name = "heating-chatbot"
chatbot_image = chatbot_name + ":latest"
simulator_name = "boiler-simulator"
simulator_image = simulator_name + ":latest"
dockerfile_path = "docker/Dockerfile"


def init_chatbot():
    """
    Initialize the chatbot Docker image and container.
    """
    build_docker_chatbot(chatbot_image, dockerfile_path)
    run_docker_chatbot(chatbot_name, network_name)


def init_simulator():
    """
    Initialize the simulator Docker image and container.
    """
    build_docker_simulator(simulator_image, dockerfile_path)
    run_docker_simulator(simulator_name, network_name)


def main():
    """
    Main function.
    """
    # Create Docker network of the two containers
    create_docker_network(network_name)

    # Create threads for each Docker container
    chatbot_thread = threading.Thread(target=init_chatbot)
    simulator_thread = threading.Thread(target=init_simulator)

    # Start the threads
    chatbot_thread.start()  # http://0.0.0.0:8501/
    simulator_thread.start()  # http://0.0.0.0:8000/

    # Wait for both threads to complete
    chatbot_thread.join()
    simulator_thread.join()


if __name__ == "__main__":
    main()
