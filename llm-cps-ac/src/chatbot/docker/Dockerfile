# Dockerfile to containerize a the ChatBot app, exposing port 8501 and setting up health checks.
# https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker

# Using python 3.10 slim image
FROM python:3.11-slim

# Set working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install all dependencies
RUN pip install --no-cache-dir -r docker/requirements.txt

# Expose port 8501
EXPOSE 8501

# Tell Docker how to test a container to check that it is still working
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Allow to configure a container that will run as an executable
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
