# Use an official Python runtime as a parent image
FROM ubuntu:20.04

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        python3.6 \
        python3.6-venv \
        python3.6-dev \
        python3-dev \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
        libpulse-dev \
        libasound2-dev \
        rustc \
        cargo \
        libjpeg-dev \
        zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a directory for your Django project
WORKDIR /app

# Copy your Django project files into the container
COPY . /app/

# Create a Python virtual environment and activate it
RUN python3.6 -m venv myenv
RUN /bin/bash -c "source myenv/bin/activate && pip install nltk==3.6.7 && python3.6 -m nltk.downloader omw-1.4 && python3.6 -m nltk.downloader stopwords && python3.6 -m nltk.downloader punkt"
RUN /bin/bash -c "source myenv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
RUN /bin/bash -c "source myenv/bin/activate && pip install gensim==3.8"

# Expose the port that the Django app will run on
EXPOSE 8000