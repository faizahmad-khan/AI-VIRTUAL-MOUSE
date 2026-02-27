# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for OpenCV, GUI (X11), and camera access
# xvfb is needed for running GUI applications in a potentially headless environment or for X11 forwarding.
# libgtk2.0-dev and libcanberra-gtk-module are often needed for OpenCV's highgui module.
# v4l-utils is for video device utilities.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    libice6 \
    libatlas-base-dev \
    ffmpeg \
    x11-apps \
    libgtk2.0-0 \
    libcanberra-gtk-module \
    v4l-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install any needed Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code into the container
COPY src/ /app/src/
COPY config.yaml /app/config.yaml
COPY QUICKSTART.md /app/QUICKSTART.md

# Set the entry point for the application.
# The `combined_ai_mouse.py` script will be executed when the container starts.
CMD ["python", "src/combined_ai_mouse.py"]
