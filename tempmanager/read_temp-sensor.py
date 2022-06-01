from datetime import datetime
from time import sleep
#from dotenv import load_dotenv
import os
import logging
import re

from influxdb import InfluxDBClient

class Config():

    def __init__(self):

        # get env-vars from .env (via docker-compose)
        self.influx_bucket = os.getenv("INFLUXDB_DB")
        self.influx_user = os.getenv("INFLUXDB_USER")
        self.influx_password = os.getenv("INFLUXDB_USER_PASSWORD")
        self.influx_url = os.getenv("INFLUXDB_URL")
    
    def connect(self):

        # establish a connection
        self.influx_client = InfluxDBClient(
            host=self.influx_url,
            port=8086,
            username=self.influx_user,
            password=self.influx_password
        )

        self.influx_client.switch_database(self.influx_bucket)

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
                point = [{
                    "measurement": "temperature",
                    "tags": {
                        "location": "raspberry"
                    },
                    "time": datetime.utcnow(),
                    "fields": {
                        "pi-temperature": pitemperature
                    }
                }]

                logging.info("Logging temperature: {} at {}".format(
                    point[0]["fields"]["pi-temperature"],
                    point[0]["time"]
                ))

                self.influx_client.write_points(point)

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
    sensor_path = os.path.join(
        "/sys/bus/w1/devices",
        sensor_id,
        "w1_slave"
    )
    sens = ReadSensor(sensor_path=sensor_path)

    # start reading from sensor
    sens()
