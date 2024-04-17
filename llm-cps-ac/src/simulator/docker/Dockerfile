# Dockerfile to containerize a the Boiler Simulator app.
# Use Xvfb (X Virtual Framebuffer) to run the tkinter app in a headless environment.

# Using python 3.11 slim image
FROM python:3.11-slim

# Set working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install tkinter, Xvfb and all dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    xvfb \
    && pip install --no-cache-dir -r docker/requirements.txt

# Set the display environment variable
ENV DISPLAY=:99

# Expose port 8000
EXPOSE 8000

# Start Xvfb and boiler simulator
CMD Xvfb :99 -screen 0 1024x768x24 & python main.py
