# Source code directory

This directory contains the source code for the `tb-optibot` project. You will find below a brief description of the different subdirectories and files.


## Subdirectories

### [chatbot](chatbot)
This directory contains the source code for the chatbot for heating system control. It includes Python scripts for handling user input, database configuration, and various functionalities of the chatbot. It also includes a `README.MD` file for more details about the chatbot.

### [demonstration](demonstration)
This directory contains example scripts showcasing certain functionalities of the project, including the OpenAI "Function call" and LangChain framework. It also includes a `README.MD` file, and each subdirectory has also its own `README.MD` file with more detailed information.

### [simulator](simulator)
This directory includes the source code for the boiler simulator. It includes Python scripts for the various components of the simulator like boiler, building, weather, etc., along with routes and models. A `README.MD` file is also included for further details about the simulator.

### `run_all.py`
This is a Python script that allows running both the heating chatbot and boiler simulator simultaneously in a local environment.

### `run_all_docker.py`
This Python script is used to run both the heating chatbot and boiler simulator simultaneously in Docker containers.


## How to Use

Each subdirectory contains specific source code files that can be run individually according to the requirements.

If you want to run both the heating chatbot and boiler simulator simultaneously, you can use `run_all.py` for a local environment and `run_all_docker.py` for Docker containers.

Please remember to use appropriate Python environments and install necessary dependencies before running the scripts. You will find more details in the `README.MD` files of each subdirectory to properly install and run the source code files.
