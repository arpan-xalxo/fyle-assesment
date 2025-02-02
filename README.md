# Fyle Backend Challenge accepted and completed with Dockerfile and a docker-compose.yml

# **Project Documentation: Building and Running the Application with Docker**

This document provides step-by-step instructions to build and run the application using Docker. Follow these steps to set up the application in a containerized environment with Docker.

---

## **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Clone the Repository](#clone-the-repository)
3. [Build the Docker Images](#build-the-docker-images)
4. [Start the Application](#start-the-application)
5. [Verify the Containers](#verify-the-containers)
6. [Access the Application](#access-the-application)
7. [Running Tests](#running-tests)
8. [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
9. [Conclusion](#conclusion)

---

## **Prerequisites**

Before you start, make sure you have the following tools installed:

- **Docker**: To containerize the application. Install Docker by following the instructions [here](https://docs.docker.com/get-docker/).
- **Docker Compose**: To manage multi-container applications. Install it by following the steps in the official [Docker Compose installation guide](https://docs.docker.com/compose/install/).
- Basic knowledge of terminal commands.

---

## **Clone the Repository**

1. Clone the project repository to your local machine.

```bash
git clone https://github.com/arpam-xalxp/fyle-assesment.git
cd fyle-assesment


Build the Docker Images

In the project directory, build the Docker images using the docker-compose command. This command will create both the application and database containers defined in the docker-compose.yml file.

sudo docker-compose build --no-cache

The --no-cache flag forces Docker to rebuild the images from scratch, ensuring you get the latest versions of all dependencies.

Start the Application
After the images are built, you can start the application and PostgreSQL database containers by running:

sudo docker-compose up

This will launch both containers, with the application running in one and the PostgreSQL database in the other. If you want to run the containers in detached mode (in the background), 

use:
sudo docker-compose up -d

Verify the Containers

To verify that the containers are running, execute the following command:

sudo docker ps

You should see both the flask_app container (your backend application) and the postgres_db container (your PostgreSQL database) listed, along with their status and the exposed ports.

Access the Application

The application will now be accessible at http://localhost:5000. You can visit this URL in your browser to see the running application.