#!/bin/bash

# check if sensor is detected:
printf "\nNumber of sensors detected:"
cat /sys/bus/w1/devices/w1_bus_master1/w1_master_slave_count

# get ID of sensor:
printf "\nID of sensor:"
cat /sys/bus/w1/devices/w1_bus_master1/w1_master_slaves

SENSOR_ID=$(cat /sys/bus/w1/devices/w1_bus_master1/w1_master_slaves)

# check temperature:
printf "\nCurrent temperature:"
cat /sys/bus/w1/devices/$SENSOR_ID/w1_slave

echo "TEMP_SENSOR_ID=$SENSOR_ID" | tee -a $pwd/.env
