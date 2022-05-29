# raspi-temperature

Setup for a DS1820 temperatur sensor using docker, influxdb and grafana for visualization (some parts are taken from https://www.kompf.de/weather/pionewiremini.html).

## Setup

To connect the temperatur sensor to the rasperry see instructions from [here](https://www.kompf.de/weather/pionewiremini.html).

To perform initial setup of the connected temperatur sensor, run

```bash
./setup_raspberry.py
```

After the reboot, run

```bash
config_sensor.sh
```

To create the dockerized framework, run

```bash
setup_docker.sh
```

Finally, to start everything, run

```bash
docker-compose up -d
```
