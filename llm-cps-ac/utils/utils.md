# Useful commands


## Poetry
Create virtual environment:
`poetry install`

Addind dependencies:
`poetry add <package-name>`

Adding dev dependencies:
`poetry add <package-name> --group dev`

Updating dependencies:
`poetry update`

Working with virtual environment:
`poetry shell`


## Pre-commit
Run all pre-commit hooks:
`pre-commit run --all-files`

Update pre-commit hooks:
`pre-commit autoupdate`


## FastAPI
Run FastAPI server:
`uvicorn main:app --reload`

Run FastAPI server with specific host and port:
`uvicorn main:app --reload --host 127.0.0.1 --port 8001`


## Python
Create virtual environment:
`python3 -m venv venv`

Activate virtual environment:
`source venv/bin/activate`

Install requirements:
`pip install -r requirements.txt`


## Set environment variable OPENAI_API_KEY
`export OPENAI_API_KEY=your-key`
