#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenAI handler for the heating control chatbot, responsible for sending and receiving messages to and from the OpenAI API.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-10"
__version__ = "1.1"
__email__ = "philippe.marziale@edu.hefr.ch"


import json
import logging
import openai

from app.config import Config


class OpenAIHandler:
    """
    Handler for the OpenAI API.
    Handles messaging and function calls to the OpenAI API.
    """

    def __init__(
        self,
        all_functions,
        functions_definitions,
        system_message,
        model=Config.GPT_MODEL,
    ):
        # Initialize the OpenAI API
        openai.api_key = Config.OPENAI_API_KEY
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")

        # Initialize the handler
        self.all_functions = all_functions
        self.functions_definitions = functions_definitions
        self.system_message = system_message
        self.model = model

    def send_message(self, query):
        """
        Send a message to the OpenAI API and receive a response.
        """
        try:
            # Send the message to the OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_message,
                    },
                    {"role": "user", "content": query},
                ],
                functions=self.functions_definitions,
            )
            message = response["choices"][0]["message"]
            total_tokens = response["usage"]["total_tokens"]
            return message, total_tokens
        except Exception as e:
            logging.error(f"Error while sending message: {e}")
            return (
                "Sorry, the OpenAI API is not available yet. Please try again later.",
                None,
            )

    def process_function_call(self, message):
        """
        Process a function call from the OpenAI API.
        """
        if message.get("function_call"):
            print(message.get("function_call"))
            function_name = message["function_call"]["name"]
            function_args_json = message["function_call"].get("arguments", {})
            function_args = json.loads(function_args_json)

            function_to_call = self.all_functions.get(function_name)

            # If the function exists, call it
            if function_to_call:
                try:
                    result = str(function_to_call(**function_args))
                    return function_name, result
                except Exception as e:
                    logging.error(f"Error while processing function call: {e}")
                    return None, None
            else:
                logging.warning(f"Function {function_name} not found")
                return None, "Sorry, I don't know how to do that."

        return None, None

    def send_response(self, query):
        """
        Send a response to the OpenAI API and handle any function calls.
        """
        message, total_tokens = self.send_message(query)
        function_name, result = self.process_function_call(message)

        # If a function call was made, send a second response with the function call
        if function_name and result:
            logging.info("Sending response with function call")
            try:
                second_response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": self.system_message,
                        },
                        {"role": "user", "content": query},
                        message,
                        {
                            "role": "function",
                            "name": function_name,
                            "content": result,
                        },
                    ],
                )
                return second_response["choices"][0]["message"]["content"], total_tokens
            except Exception as e:
                logging.error(f"Error while sending response: {e}")
                return (
                    "Sorry, the OpenAI API is not available yet. Please try again later.",
                    None,
                )

        else:
            logging.info("Sending response without function call")
            return message["content"], total_tokens
