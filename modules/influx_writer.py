#!/usr/bin/env python3
import logging
import json
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point
from config import Config
logger = logging.getLogger(__name__)



def main(data):
    data = json.loads(json.dumps(data, indent=4))

    writer('disks', data)
    writer('cpu', data)
    writer('ram', data)
    writer('swap', data)


def writer(metric, data):
    if metric == 'disks':
        for keys, values in data[metric].items():
            point = Point(keys)
            point.tag("Metric", metric)
            point.tag("Hostname", Config.hostname)
            for key, value in values.items():
                point.field(key, value)
            with InfluxDBClient(url=Config.influx_url, token=Config.influx_token, org=Config.influx_org) as client:
                with client.write_api(write_options=SYNCHRONOUS) as writer:
                    try:
                        writer.write(bucket=Config.influx_bucket, record=[point])
                    except InfluxDBError as e:
                        logging.exception(f"Error while writing to influxdb: {e}")
    else:
        point = Point(metric)
        point.tag("Metric", metric)
        point.tag("Hostname", Config.hostname)
        for key, value in data[metric].items():
            point.field(key, value)
        with InfluxDBClient(url=Config.influx_url, token=Config.influx_token, org=Config.influx_org) as client:
            with client.write_api(write_options=SYNCHRONOUS) as writer:
                try:
                    writer.write(bucket=Config.influx_bucket, record=[point])
                except InfluxDBError as e:
                    logging.exception(f"Error while writing to influxdb: {e}")