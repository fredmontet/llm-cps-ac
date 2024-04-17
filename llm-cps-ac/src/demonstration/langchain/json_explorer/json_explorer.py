#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example of usage of the langchain framework to explore a JSON file.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-03"
__version__ = "1.0"
__email__ = "philippe.marziale@edu.hefr.ch"


import json
import openai
import os

from dotenv import load_dotenv

from langchain.agents import create_json_agent
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.chat_models import ChatOpenAI
from langchain.tools.json.tool import JsonSpec


# Load .env file and get OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Load json data
with open("src/demonstration/langchain/json_explorer/users.json") as f:
    data = json.load(f)

# Define how to interact with json data
json_spec = JsonSpec(dict_=data, max_value_length=4000)

# Interact with the JsonSpec
json_toolkit = JsonToolkit(spec=json_spec)

# Create a json agent
# The created agent will be used to run queries against the loaded JSON data.
json_agent_executor = create_json_agent(
    llm=ChatOpenAI(), toolkit=json_toolkit, verbose=True
)

# Trigger the agent to search for the information related to "Julie's favorite temperatures" in the JSON data
json_agent_executor.run("What are Julie's favorite temperatures?")
