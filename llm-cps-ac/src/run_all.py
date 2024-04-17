#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run the heating chatbot and boiler simulator simultaneously locally.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-09"
__version__ = "1.0"
__email__ = "philippe.marziale@edu.hefr.ch"


import subprocess
import threading
import os


def run_chatbot():
    """
    Run the heaating chatbot.
    """
    os.chdir("src/chatbot")
    subprocess.run(["streamlit", "run", "main.py"])


def run_simulator():
    """
    Run the boiler simulator.
    """
    os.chdir("../simulator")
    subprocess.run(["python", "main.py"])


def main():
    """
    Main function to run the heating chatbot and the boiler simulator in the same time.
    """
    # Change current directory to the directory of this script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.expanduser(script_directory + "/../"))

    # Initialize threads
    chatbot_thread = threading.Thread(target=run_chatbot)
    simulator_thread = threading.Thread(target=run_simulator)

    # Start threads
    chatbot_thread.start()
    simulator_thread.start()

    # Wait for both threads to complete
    chatbot_thread.join()
    simulator_thread.join()


if __name__ == "__main__":
    main()
