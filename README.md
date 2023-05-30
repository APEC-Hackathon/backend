# backend

This project is a FastAPI backend for CollabMarket.

## Deployment

The backend is deployed at http://172.104.229.42:8000/. Swagger API documentation is available at http://172.104.229.42:8000/docs and Redoc API documentation is available at http://172.104.229.42:8000/redoc.

## Prerequisite

Before running the backend, ensure that you have the following installed on your local machine:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository: `git clone https://github.com/APEC-Hackathon/backend.git`

2. Navigate to the project directory: `cd fastapi-backend`

3. Rename or copy the `.env_sample` file to `.env` and fill in the environment variables.

4. Run the following command to build and start the Docker containers: `docker-compose up --build`. This command will pull the necessary Docker images, build the backend container, and start the services defined in the `docker-compose.yml` file.

Once the containers are up and running, you can access the FastAPI backend at http://localhost:8000. The backend will be connected to a PostgreSQL database running in a separate container.
