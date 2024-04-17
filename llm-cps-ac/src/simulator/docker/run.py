#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run the previously built Docker image of the boiler simulator application,
expose the port 8000 to the host and display the simulator screen.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-09"
__version__ = "1.1"
__email__ = "philippe.marziale@edu.hefr.ch"


import subprocess


network_name = "optibot-network"
simulator_name = "boiler-simulator"


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


def run_docker_simulator(simulator_name, network_name):
    """
    Run the Docker's simulator image (remove it before if it already exists).
    """
    if check_docker_container(simulator_name):
        subprocess.run(["docker", "rm", "-f", simulator_name])

    # Allow the simulator to display on the host X's server
    subprocess.run(["xhost", "+localhost"])

    # Run the simulator container
    subprocess.run(
        [
            "docker",
            "run",
            "--name",
            simulator_name,
            "--network",
            network_name,
            "-e",
            f"PORT=8000",
            "-e",
            f"DISPLAY=host.docker.internal:0",
            "-p",
            "8000:8000",
            simulator_name + ":latest",
        ]
    )


if __name__ == "__main__":
    create_docker_network(network_name)
    run_docker_simulator(simulator_name, network_name)
