import logging
import json
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point
from .config import Config

logger = logging.getLogger(__name__)
config = Config()


def main(data):
    metrics = ['disks', 'cpu', 'ram', 'swap', 'net_interfaces', 'docker']
    with InfluxDBClient(url=config.agent_influx_url, token=config.agent_influx_token,
                        org=config.agent_influx_org) as client:
        for metric in metrics:
            write_to_influxdb(metric, data, client)


def write_to_influxdb(metric, data, client):
    point = Point(metric)
    point.tag("Metric", metric)
    point.tag("Hostname", config.agent_hostname)

    if metric in ['disks', 'net_interfaces', 'docker']:
        for keys, values in data[metric].items():
            for key, value in values.items():
                point.field(key, value)
    else:
        for key, value in data[metric].items():
            point.field(key, value)

    try:
        logger.info(point)
        with client.write_api(write_options=SYNCHRONOUS) as writer:
            writer.write(bucket=config.agent_influx_bucket, record=[point])
    except Exception as e:
        logger.warning(f"Error while writing to InfluxDB: {e}")