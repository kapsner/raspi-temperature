#!/bin/bash

# load 1-wire drivers:
echo "dtoverlay=w1-gpio,gpiopin=4,pullup=on" | sudo tee -a /boot/config.txt

sudo modprobe wire
sudo modprobe w1-gpio pullup=1
sudo modprobe w1-therm

echo "wire" | sudo tee -a /etc/modules
echo "w1-gpio pullup=1" | sudo tee -a /etc/modules
echo "w1-therm" | sudo tee -a /etc/modules

# reboot
printf "\nRebooting system in 5 seconds"
sleep 5
sudo reboot
