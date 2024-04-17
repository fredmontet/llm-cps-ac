#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chatbot using Streamlit, LangChain and OpenAI's APIs.

Run the application with:
    streamlit run main.py
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-13"
__version__ = "1.3"


import json
import os
import streamlit as st
from streamlit_chat import message as st_message

from app.functions import all_functions
from app.handler import OpenAIHandler
from app.vector_db import create_vectorstore
from app.sql_db import init_db
from app.config import Config, ChatbotPrompt


# Get the functions definitions from the JSON file
with open(Config.FNCT_DEF_PATH, "r") as file:
    functions_definitions = json.load(file)["functions"]

# Initialize the OpenAIHandler
handler = OpenAIHandler(
    all_functions, functions_definitions, ChatbotPrompt.system_message
)

# Create the vectorstore if it doesn't exist
if not os.path.exists(Config.VECTOR_STORE_PATH):
    create_vectorstore()

# Initialize the (SQL) database
init_db()


def run_conversation(query):
    """
    Run a conversation with the heating system using LangChain and OpenAI's chat models.
    """
    # Get the response from the LLM and the total token count
    response, total_tokens = handler.send_response(query)

    # Add tokens from the response to the total token count
    st.session_state.token_count += total_tokens

    # Return the response
    return response


def main():
    """
    Main function of the chatbot, responsible for the Streamlit UI.
    """
    # Initialize Streamlit title and description
    st.title("♨️💬 Heating systems Chatbot")
    st.write(
        "**Hi, I'm « Opti » ! Your intelligent and informed companion to the heating control system. "
        + "I'm here to answer your questions about the heating system. If you wish, I can also modify "
        + "various parameters such as setpoint temperature, boiler power, and many more!**"
    )

    # Initialize the chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Initialize the total token count
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0

    # Display the chat history
    for i, chat in enumerate(st.session_state.history):
        st_message(**chat, key=str(i))

    def generate_answer():
        """
        Generate the bot's answer and add it to the chat history.
        """
        # Get the user's message
        user_message = st.session_state.input_text

        # Get previous user question and bot answer
        if len(st.session_state.history) > 0:
            prev_bot_answer = st.session_state.history[-1]["message"][:200]
            prev_user_question = st.session_state.history[-2]["message"]
        else:
            prev_user_question = ""
            prev_bot_answer = ""

        # Create the next message to send to the bot (history depth of 1)
        next_message = f"History:\nHuman: {prev_user_question}\nAssistant: {prev_bot_answer}\nQuestion: {user_message}"

        # Generate the bot's answer
        answer = run_conversation(next_message)

        # Add the user's message and the bot's answer to the chat history
        st.session_state.history.append({"message": user_message, "is_user": True})
        st.session_state.history.append({"message": answer, "is_user": False})

        # Clear the input text
        st.session_state.input_text = ""

    # Create a text input field for the user's message
    st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)

    # Display the total token count
    st.caption(f"Used {st.session_state.token_count} tokens")


if __name__ == "__main__":
    main()
