#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build a Docker image for the boiler simulator application.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-09"
__version__ = "1.1"
__email__ = "philippe.marziale@edu.hefr.ch"


import os
import subprocess


image_name = "boiler-simulator:latest"
dockerfile_path = "docker/Dockerfile"


def check_docker_image(image_name):
    """
    Check if a Docker image exists.
    """
    result = subprocess.run(
        ["docker", "images", "-q", image_name], capture_output=True, text=True
    )
    return result.stdout.strip() != ""


def build_docker_simulator(image_name, dockerfile_path):
    """
    Build the Docker's simulator image (remove it before if it already exists).
    """
    if check_docker_image(image_name):
        subprocess.run(["docker", "rmi", "-f", image_name])
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.expanduser(script_directory + "/../"))
    subprocess.run(["docker", "build", "-t", image_name, "-f", dockerfile_path, "."])


if __name__ == "__main__":
    build_docker_simulator(image_name, dockerfile_path)
