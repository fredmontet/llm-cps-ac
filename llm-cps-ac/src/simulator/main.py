#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main module for the heating simulation.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-10"
__version__ = "3.1"
__email__ = "philippe.marziale@edu.hefr.ch"


import threading

from fastapi import FastAPI
from app.routes import router
from uvicorn import run

from app.instances import (
    building,
    boiler,
    regulator,
    TIME_STEP,
)
from app.simulator import Simulator


# Initialize the simulator objects
simulator = None

# Initialize the FastAPI application and include the router
app = FastAPI()
app.include_router(router)


def run_simulator():
    """
    Run the simulation.
    """
    # Run the simulation with the initialized boiler, building, regulator, weather and time step
    global simulator
    simulator = Simulator(
        boiler,
        building,
        regulator,
        TIME_STEP,
        built_in_screen=False,
    )


def run_api():
    """
    Run the FastAPI application.
    """
    run(app, host="0.0.0.0", port=8000)


def main():
    """
    Main function to run the simulation and the API.
    """
    # Create threads for the API
    api_thread = threading.Thread(target=run_api, args=())

    # Start the threads
    api_thread.start()

    # Run the simulator in the main thread
    run_simulator()

    # Wait for the API thread to complete
    api_thread.join()


if __name__ == "__main__":
    main()
