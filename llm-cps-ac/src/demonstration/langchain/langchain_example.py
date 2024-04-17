#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example of usage of the langchain framework.
This Python script utilizes the OpenAI GPT model to generate articles automatically based on user-provided topics.
By entering a topic through the Streamlit interface, the script generates an article title and performs research
on Wikipedia. The gathered information is then used to create the content of the article.

Inspired by this video: https://youtu.be/MlK6SIjcjE8 (Nicholas Renotte)
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-06-27"
__version__ = "1.0"
__email__ = "philippe.marziale@edu.hefr.ch"


import os
import openai
import streamlit as st

from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper


# Load .env file and get OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def setup_streamlit():
    """Setup streamlit UI."""
    st.title("🦜🔗 Article GPT Creator")
    return st.text_input("Plug in your prompt here")


def setup_prompt_templates():
    """Initialize prompt templates."""
    title_template = PromptTemplate(
        input_variables=["topic"], template="write me a title for an article on {topic}"
    )

    article_template = PromptTemplate(
        input_variables=["title", "wikipedia_research"],
        template="write me an article based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} ",
    )

    return title_template, article_template


def setup_memory_buffers():
    """Initialize conversation buffer memories."""
    title_memory = ConversationBufferMemory(
        input_key="topic", memory_key="chat_history"
    )
    article_memory = ConversationBufferMemory(
        input_key="title", memory_key="chat_history"
    )

    return title_memory, article_memory


def setup_llm_chains(title_template, article_template, title_memory, article_memory):
    """Initialize LLM chains."""
    llm = OpenAI(temperature=0.8)
    title_chain = LLMChain(
        llm=llm,
        prompt=title_template,
        verbose=True,
        output_key="title",
        memory=title_memory,
    )
    article_chain = LLMChain(
        llm=llm,
        prompt=article_template,
        verbose=True,
        output_key="article",
        memory=article_memory,
    )

    return title_chain, article_chain


def run_app(prompt, title_chain, article_chain, title_memory, article_memory):
    """Run app if there's a prompt."""
    if not prompt:
        st.warning("Please enter a prompt.")
        return

    wiki = WikipediaAPIWrapper()
    try:
        title = title_chain.run(prompt)
        wiki_research = wiki.run(prompt)
        article = article_chain.run(title=title, wikipedia_research=wiki_research)

        st.write(title)
        st.write(article + " ...")

        with st.expander("Title History"):
            st.info(title_memory.buffer)

        with st.expander("Article History"):
            st.info(article_memory.buffer)

        with st.expander("Wikipedia Research"):
            st.info(wiki_research)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


def main():
    """Main entry point of the application."""
    prompt = setup_streamlit()
    title_template, article_template = setup_prompt_templates()
    title_memory, article_memory = setup_memory_buffers()
    title_chain, article_chain = setup_llm_chains(
        title_template, article_template, title_memory, article_memory
    )
    run_app(prompt, title_chain, article_chain, title_memory, article_memory)


if __name__ == "__main__":
    main()
    # streamlit run src/langchain/langchain_example.py
