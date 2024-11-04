#!/bin/bash

# Echo message for changing directory 
echo "Changing directory to 'Rental/rental_backend'..." 
cd Rental/rental_backend
 
# Echo message for pulling latest changes from git 
echo "Pulling latest changes from git..." 
git pull 
 
# Variables
COMPOSE_FILE="docker-compose.yml"

# Build the Docker image using Docker Compose
echo "Building the Docker image with Docker Compose..."
docker-compose -f $COMPOSE_FILE build

if [ $? -ne 0 ]; then
    echo "Error: Failed to build the Docker image using Docker Compose."
    exit 1
fi

# Stop and remove old containers
echo "Stopping and removing old containers..."
docker-compose -f $COMPOSE_FILE down

# Start new containers
echo "Running new containers with Docker Compose..."
docker-compose -f $COMPOSE_FILE up -d

if [ $? -ne 0 ]; then
    echo "Error: Failed to run the Docker containers using Docker Compose."
    exit 1
fi

# Clean up unused images and containers
echo "Cleaning up unused images and containers..."
docker system prune -f

echo "Operation completed successfully."