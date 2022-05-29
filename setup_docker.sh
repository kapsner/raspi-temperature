#!/bin/bash

# build docker container
docker build -f Dockerfile -t tempmanager .

# start framework for initial setup
docker-compose up -d

# wait 30 seconds
sleep 30

# stop framework
docker-compose down
