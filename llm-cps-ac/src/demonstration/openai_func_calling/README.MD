# OpenAI "Function calling" demonstration

This directory contains the codes of the demonstration of the "function calling" feature of OpenAI's GPT-3.5 API, developed in Python.


## Requirements

- Python 3.8 or later
- Poetry (and defined dependencies)
- OpenAI with an API key


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

1. Run the OpenAI's demonstration:

```shell
python src/demonstration/openai_func_calling/openai_func_calling_example.py
```

2. Run the weather forecast demonstration:

```shell
python src/demonstration/openai_func_calling/openai_func_calling_weather.py
```


## Files

- `openai_func_calling_example.py`: OpenAI's demonstration of the "function calling" feature.
- `openai_func_calling_weather.py`: Weather forecast demonstration using the "function calling" feature of OpenAI.
- `weather.py`: Script that retrieves the current temperature for a given address by leveraging the Open-Meteo API for weather data and the OpenStreetMap Nominatim API for geocoding (taken from PS6).
