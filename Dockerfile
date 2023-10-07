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
RUN python3.6 -m venv myenv && \
    source myenv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Replace 'HOST' with '<db_ipaddress>' in settings.py
RUN sed -i "s/'HOST': '[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+',/'HOST': '<db_ipaddress>',/g" meetia/settings.py

# Replace '<db_ipaddress>' with the actual IP address
RUN sed -i "s/<db_ipaddress>/$(docker inspect meetiadb --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')/g" meetia/settings.py

# Create database migrations
RUN python3.6 manage.py makemigrations

# Apply database migrations
RUN python3.6 manage.py migrate

# Expose the port that the Django app will run on
EXPOSE 8000

# Start the Django server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
