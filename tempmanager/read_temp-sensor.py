from datetime import datetime
from time import sleep
#from dotenv import load_dotenv
import os
import logging
import re

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class Config():

    def __init__(self):

        # get env-vars from .env (via docker-compose)
        self.influx_org = os.getenv("DOCKER_INFLUXDB_INIT_ORG")
        self.influx_bucket = os.getenv("DOCKER_INFLUXDB_INIT_BUCKET")
        self.influx_token = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
        self.influx_url = os.getenv("INFLUXDB_URL")
    
    def connect(self):

        # establish a connection
        self.influx_client = InfluxDBClient(
            url=self.influx_url,
            token=self.influx_token,
            org=self.influx_org
        )

        # instantiate the WriteAPI 
        self.influx_write_api = self.influx_client.write_api(
            write_options=SYNCHRONOUS
        )

class ReadSensor(Config):

    def __init__(self, sensor_path):
        
        super().__init__()

        # sensor-path
        self.sensor_path = sensor_path

        # establish connection to influx-db
        self.connect()
    
    def __call__(self):

        while True:
            pitemperature = self.read_sensor()

            if pitemperature == float:
                point = Point("temperature") \
                    .tag("location", "raspberry") \
                    .field("pi-temperature", pitemperature) \
                    .time(datetime.utcnow(), WritePrecision.NS)

                self.influx_write_api.write(
                    self.influx_bucket,
                    self.influx_org,
                    point
                )

            # wait 60 seconds
            sleep(60)

    def read_sensor(self):
        # with some adaptions from
        # https://www.kompf.de/weather/pionewiremini.html
        value = None

        try:
            f = open(self.sensor_path, "r")
            line = f.readline()
            if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
                line = f.readline()
                m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
            if m:
                value = float(m.group(2)) / 1000.0
            f.close()

        except Exception as e:
            logging.error(e)

        return value

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    
    # path to 1-wire sensor data
    sensor_id = os.getenv("TEMP_SENSOR_ID")
    if len(sensor_id) == 0 or sensor_id == "":
        raise Exception("No sensor_id found")
    sensor_path = os.join.path(
        "/sys/bus/w1/devices",
        sensor_id,
        "w1_slave"
    )
    sens = ReadSensor(sensor_path=sensor_path)

    # start reading from sensor
    sens()
