#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create and load a vector store used by the chatbot.

https://python.langchain.com/docs/modules/data_connection/vectorstores/
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-04"
__version__ = "1.0"
__email__ = "philippe.marziale@edu.hefr.ch"


import pickle

from app.config import Config

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS


def create_vectorstore():
    """
    Create a vector store from text documents using LangChain and OpenAI embeddings.
    """
    # Load all .txt files in the data folder
    loader = DirectoryLoader(
        Config.DATA_FOLDER_PATH,
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True,
    )
    raw_documents = loader.load()

    # Split the text documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
    )
    documents = text_splitter.split_documents(raw_documents)

    # Create embeddings for each document
    embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)

    # Store embeddings into a FAISS vector store
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Serialize and store the vector store into a file
    with open(Config.VECTOR_STORE_PATH, "wb") as f:
        pickle.dump(vectorstore, f)


def get_vectorstore():
    """
    Function to load the vector store from disk. If it doesn't exist, create it.
    """
    try:
        # Attempt to load the vector store
        with open(Config.VECTOR_STORE_PATH, "rb") as file:
            vectorstore = pickle.load(file)

    except FileNotFoundError:
        # If the vector store doesn't exist, create it and then load it
        print("Vectorstore not found. Creating one.")
        create_vectorstore()
        with open(Config.VECTOR_STORE_PATH, "rb") as file:
            vectorstore = pickle.load(file)

    return vectorstore
