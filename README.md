# MeetIA

## Project Description

MeetIA is a platform designed for efficient and productive collaboration in modern workplaces. It simplifies meeting management, enhances communication, and automates transcription and summarization of meeting recordings. This tool is the key to boosting productivity and streamlining teamwork.

## Key Features

- **Meeting Management:** Easily schedule, invite participants, and keep track of meetings.
- **Automatic Transcription:** Meeting recordings are transcribed automatically.
- **NLP Summarization:** Summarize meeting content using NLP libraries.
- **Secure Data Storage:** Safely store meeting data and transcripts.
- **User-Friendly Interface:** Intuitive and easy to navigate.

## Benefits

- **Boost Productivity:** Streamline meeting tasks and save time.
- **Improve Communication:** Enhance collaboration and discussion.
- **Effortless Documentation:** Automate recording and summarization.
- **Data-Driven Insights:** Access historical data for decision-making.
- **Security:** Protect sensitive data with robust access controls.

## Architecture

MeetIA consists of two core services orchestrated using Docker Compose:

### Database Service (`db`):

- Utilizes the latest MySQL image (`mysql:latest`).
- Named **meetiadb**.
- Environment variables configure the MySQL instance.
- Utilizes the **mysql_data** volume for data persistence.
- Connected to the **mynet** network.

### Application Service (`appserver`):

- Depends on **db**.
- Builds from a Dockerfile.
- Listens on port 8000.
- Uses environment variables for configuration.
- Handles media files with the **media-volume** volume.
- Connected to the **mynet** network.

### Volumes

- Two named volumes: **mysql_data** for MySQL data and **media-volume** for managing media files.

### Network

- A bridge network named **mynet** facilitates service communication.

This architecture simplifies meeting management, automates transcription, and provides secure data storage, ensuring a seamless and productive collaborative work environment.

## Installation

### Prerequisites

Before you begin, please ensure that you have Docker and Docker Compose installed on your system.

### Step 1: Run Docker Compose

We'll use Docker Compose to set up the components outlined in the architecture section. Follow these steps:

1. Open a terminal.

2. Navigate to the root directory of your project.

3. Run the following command to start the services:

   ```bash
   docker-compose up
This command will orchestrate the database and application services, creating the necessary containers.

### Step 2: Create the Admin Superuser
Once the services are up and running, you can create the admin superuser by executing the following command:
   ```bash
   docker exec -it meetiaappserver /bin/bash -c "source myenv/bin/activate && python3 manage.py createsuperuser"
   ```
This command opens a shell within the meetiaappserver container, activates the virtual environment, and creates the admin superuser.

### Step 3: Create MeetIA Users
With the admin superuser created, you can now access the Django admin interface to add MeetIA users:

1. Open your web browser.

2. Navigate to the admin login page by visiting: [Admin](http://localhost:8000/admin/login/?next=/admin/)

3. Log in using the credentials of the admin superuser created in Step 2.

4. In the admin interface, you can add, manage, and configure MeetIA users as needed.

### Step 4: Access MeetIA
Now that you've set up the system and created users, you can access MeetIA by visiting: [Home](http://localhost:8000)

You're all set! MeetIA is up and running, and users can start connecting and collaborating.
