import time
import random
from influxdb import InfluxDBClient


def write():
    json_body = [
        {
            "measurement": "temperature",
            "tags": {
                "environment": "flower_tent",
            },
            "fields": {
                "value": random.uniform(60, 80)
            }
        },
        {
            "measurement": "relative_humidity",
            "tags": {
                "environment": "flower_tent",
            },
            "fields": {
                "value": random.uniform(25, 50)
            }
        },
    ]

    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'garden')
    client.write_points(json_body)

def main():
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'garden')
    client.create_database('garden')

    while True:
        print "writing normal flower data"
        write()
        time.sleep(10)

if __name__ == "__main__":
    main()    
