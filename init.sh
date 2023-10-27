#!/bin/bash

# Add the deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa

# Update package information
sudo apt-get update

# Install Python 3.6
sudo apt-get install python3.6

# Install Python 3.6 venv
sudo apt install python3.6-venv

# Install Python 3.6 development headers
sudo apt-get install python3.6-dev

# Create a Python virtual environment
python3.6 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Replace 'HOST' with '<db_ipaddress>' in settings.py
sed -i "s/'HOST': '[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+',/'HOST': '<db_ipaddress>',/g" meetia/settings.py

# Start Docker Compose
docker-compose up -d

# Replace '<db_ipaddress>' with the actual IP address
sed -i "s/<db_ipaddress>/$(docker inspect meetiadb --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')/g" meetia/settings.py

# Install pkg-config
sudo apt install pkg-config 

# Install audio libs
sudo apt-get install libpulse-dev libasound2-dev

# Set MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS environment variables
export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags`
export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`

# Install Rust and Cargo
sudo apt install rustc cargo

# Install libjpeg and zlib development libraries
sudo apt install libjpeg-dev zlib1g-dev

# Download NLTK data
python3.6 -m nltk.downloader omw-1.4
python3.6 -m nltk.downloader stopwords
python3.6 -m nltk.downloader punkt

# Install Python package requirements
pip3 install -r requirements.txt

# Create database migrations
python3.6 manage.py makemigrations

# Apply database migrations
python3.6 manage.py migrate