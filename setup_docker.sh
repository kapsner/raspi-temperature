#!/bin/bash

# build docker container
docker build -f Dockerfile -t tempmanager .

# start framework for initial setup
docker run --rm \
  -e INFLUXDB_DB=$INFLUXDB_DB \
  -e INFLUXDB_ADMIN_USER=$INFLUXDB_ADMIN_USER \
  -e INFLUXDB_ADMIN_PASSWORD=$INFLUXDB_ADMIN_PASSWORD \
  -e INFLUXDB_USER=$INFLUXDB_USER \
  -e INFLUXDB_USER_PASSWORD=$INFLUXDB_USER_PASSWORD \
  --env-file ./.env \
  -v ./influxdb-volume/data:/var/lib/influxdb \
  -v ./influxdb-volume/config:/etc/influxdb \
  influxdb:1.8 \
  /init-influxdb.sh
