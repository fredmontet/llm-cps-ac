# LangChain demonstration

This directory contains the code of a simple LangChain app, developed in Python, aiming to generate articles based on user-provided topics.


## Requirements

- Python 3.8 or later
- Poetry (and defined dependencies)
- Langchain
- OpenAI with an API key
- Streamlit
- Wikipedia
- Tiktoken


## Installation

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


## Usage

1. Run the streamlit app:

```shell
streamlit run src/demonstration/langchain/langchain_example.py
```

2. Run the JSON explorer example:

```shell
python src/demonstration/langchain/json_explorer/json_explorer.py
```


## Files

- `langchain_example.py`: Streamlit app to generate articles by generating title based on user-provided topics and conducting research on Wikipedia, subsequently using the gathered information to generate the article content.
- [json_explorer](json_explorer): Folder that contains an exemple of usage of the langchain framework to explore a JSON file.
  - `json_explorer.py`: Main file of the example.
  - `users.json`: List of users with their preferred temperatures and schedule.
