#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example of a Python code that uses the OpenAI API to call the "get_current_weather" function,
originally defined in the weather.py module itself taken from PS6 - AppGPT.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-06-26"
__version__ = "1.0"
__email__ = "philippe.marziale@edu.hefr.ch"


import json
import openai
import os
from dotenv import load_dotenv
from weather import get_weather, geocode, get_current_time


# Load .env file and get OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API parameters
MODEL = "gpt-3.5-turbo-0613"
TEMPERATURE = 0.4


def request_ChatGPT_API(messages, functions, function_call):
    """
    Request the ChatGPT API with the given prompt using the "Function calling" feature.
    """
    completion = openai.ChatCompletion.create(
        model=MODEL,
        temperature=TEMPERATURE,
        messages=messages,
        functions=functions,
        function_call={
            "name": function_call,
        },
    )
    return completion


def get_current_weather(location):
    """
    Get the current weather in the given location.
    """
    latitude, longitude = geocode(location)
    current_time = get_current_time()
    today_temp = get_weather(latitude, longitude, current_time)
    return today_temp, current_time


if __name__ == "__main__":
    # User prompt
    prompt = "Describe today's weather in Fribourg (CH)"

    # Prepare the request parameters for the weather API
    messages = [{"role": "user", "content": prompt}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. Bulle, FR",
                    },
                },
                "required": ["location"],
            },
        }
    ]
    function_call = functions[0]["name"]

    # Send the conversation and functions's description to GPT
    completion = request_ChatGPT_API(messages, functions, function_call)
    response_message = completion["choices"][0]["message"]

    # Get the function's arguments and location (address)
    arguments = json.loads(response_message["function_call"]["arguments"])
    location = arguments["location"]

    # Check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Call the function and get the weather
        today_temp, current_time = get_current_weather(location)
        second_prompt = f"Current time is {current_time.strftime('%Y-%m-%dT%H:%M')}"

        # Append the conversation with the function's result
        messages.extend(
            [
                response_message,
                {"role": "function", "name": function_call, "content": str(today_temp)},
                {"role": "user", "content": second_prompt},
            ]
        )

        # Send the conversation and functions's answer to GPT
        second_response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
        )

        # Print the response
        print(second_response["choices"][0]["message"]["content"])
    else:
        # Print the location (address)
        print(location)
