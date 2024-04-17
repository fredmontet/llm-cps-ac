# ChatBot for heating control system

*« Opti » is an intelligent and informed companion to the heating control system. His role is to answer questions about the heating system. He can also modify various parameters such as setpoint temperature, boiler power, and many more!*

This project is based on the [OpenAI's GPT-3-5 model](https://platform.openai.com/docs/models) to create an interactive chatbot for controlling the heating system. The application is built using the [LangChain](https://python.langchain.com/) and [Streamlit](https://streamlit.io/) framework. It also uses OpenAI "Function calling" feature, a SQL database for users data, and a VectorDB for specific / additional data.


## Requirements

- Python 3.11 or later
- Poetry (and defined dependencies)
- OpenAI with an API key
- Langchain
- FAISS
- SQLALchemy
- tiktoken
- Streamlit and Streamlit chat


## Project structure

- [app](app): Chatbot application
  - `config.py`: Configuration file (constants and prompts)
  - `functions_definitions.json`: Definitions of callable functions
  - `functions.py`: Functions that can be called by the chatbot
  - `handler.py`: OpenAI handler, responsible for the communication with OpenAI
  - `sql_db.py`: SQL database used to store users data
  - `vector_db.py`: Vector database used to store specific data
- [data](data): Data used by the chatbot
  - `FAQ.txt`: Some frequently asked questions specific to the heating system
  - _`users.db`: SQLite database containing users data, auto generated_
  - _`vectorstore.pkl`: Vector database containing specific data, auto generated_
- [docker](docker): Docker's files to run the chatbot into a container
  - `build.py`: Build the Docker image
  - `Dockerfile`: Instructions to build the Docker image
  - `requirements.txt`: Python dependencies
  - `run.py`: Run the Docker image
- `main.py`: Main file to run the chatbot using Streamlit GUI


## Local installation

1. Clone the repository or download the source code:

```shell
git clone https://gitlab.forge.hefr.ch/philippe.marziale/tb-optibot.git
```

2. Create a virtual environment using poetry:

```shell
poetry install
```

3. Activate the virtual environment:

```shell
poetry shell
```

4. Set your OpenAI API key in a `.env` file:
```ini
OPENAI_API_KEY=your_openai_api_key_here
```

5. Navigate to the project folder:

```bash
cd src/chatbot
```

6. Run the chatbot:

```shell
streamlit run main.py
```


## Docker installation

1. Clone the repository or download the source code:

```shell
git clone https://gitlab.forge.hefr.ch/philippe.marziale/tb-optibot.git
```

2. Set your OpenAI API key in a `.env` file:
```ini
OPENAI_API_KEY=your_openai_api_key_here
```

3. Install `dotenv` module:

```shell
pip install python-dotenv
```

4. Navigate to the project folder:

```bash
cd src/chatbot
```

5. Build the Docker image:

```shell
python docker/build.py
```

6. Run the Docker container:

```shell
python docker/run.py
```


## Usage and functionalities

1. Open your browser and go to the URL displayed in the terminal.
2. Ask your question to the chatbot.
3. The chatbot will answer your question.
4. You can also ask the chatbot to perform an action like change the temperature to a specific value.
5. The chatbot will perform the action and answer you.
