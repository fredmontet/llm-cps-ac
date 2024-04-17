#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
In the example below, we sent the function response back to the model and let it decide
the next step. It responded with a user-facing message which was telling the user the
temperature in Boston, but depending on the query, it may choose to call a function again.

For example, if you ask the model 'Find the weather in Boston this weekend, book dinner for two
on Saturday, and update my calendar' and provide the corresponding functions for these queries,
it may choose to call them back to back and only at the end create a user-facing message.

If you want to force the model to generate a user-facing message, you can do so by setting
`function_call: "none"` (if no functions are provided, no functions will be called).

The basic sequence of steps for function calling is as follows:
1. Call the model with the user query and a set of functions defined in the functions parameter.
2. The model can choose to call a function; if so, the content will be a stringified JSON object
   adhering to your custom schema (note: the model may generate invalid JSON or hallucinate parameters).
3. Parse the string into JSON in your code, and call your function with the provided arguments if they exist.
4. Call the model again by appending the function response as a new message, and let the model
   summarize the results back to the user.
"""

__author__ = "OpenAI"
__date__ = "2023-06"
__version__ = "1.0"


import json
import openai
import os
from dotenv import load_dotenv


# Load .env file and get OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        print(messages)
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response


if __name__ == "__main__":
    gpt_output = run_conversation()
    print(gpt_output["choices"][0]["message"]["content"])
