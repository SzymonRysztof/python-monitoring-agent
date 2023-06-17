import logging
import json
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point
from .config import Config

logger = logging.getLogger(__name__)
config = Config()


def main(data):
    with InfluxDBClient(url=config.agent_influx_url, token=config.agent_influx_token,
                        org=config.agent_influx_org) as client:
        write_to_influxdb(data, client)


def write_to_influxdb(data, client):
    points = []
    cpu_metrics = data['cpu']
    ram_metrics = data['ram']
    swap_metrics = data['swap']
    docker_container_metrics = data['docker']['containers']
    docker_image_metrics = data['docker']['images']
    docker_system_metrics = data['docker']['system']
    net_metrics = data['net_interfaces']
    disks_metrics = data['disks']
    hostname = config.agent_hostname

    # System metrics
    system_metric = {
        'measurement': 'system_metrics',
        'fields': {
            'cpu_user': cpu_metrics['user'],
            'cpu_system': cpu_metrics['system'],
            'cpu_idle': cpu_metrics['idle'],
            'cpu_iowait': cpu_metrics['iowait'],
            'cpu_current': cpu_metrics['current'],
            'cpu_max': cpu_metrics['max'],
            'cpu_min': cpu_metrics['min'],
            'cpu_1m': cpu_metrics['1m'],
            'cpu_5m': cpu_metrics['5m'],
            'cpu_15m': cpu_metrics['15m'],
            'cpu_utilization': cpu_metrics['utilization'],
            'cpu_temperature': cpu_metrics['temperature'],
            'cpu_processors': cpu_metrics['processors'],
        },
        'tags': {
            'hostname': hostname,
        }
    }
    points.append(system_metric)
    logger.info('System metric prepared')
    logger.debug(system_metric)

    # RAM metrics
    ram_metric = {
        'measurement': 'ram_metrics',
        'fields': {
            'ram_total': ram_metrics['total'],
            'ram_used': ram_metrics['used'],
            'ram_free': ram_metrics['free'],
            'ram_cached': ram_metrics['cached'],
            'ram_buffers': ram_metrics['buffers'],
            'ram_percent': ram_metrics['percent'],
        },
        'tags': {
            'hostname': hostname,
        }
    }
    points.append(ram_metric)
    logger.info('RAM metric prepared')
    logger.debug(ram_metric)

    # Swap metrics
    swap_metric = {
        'measurement': 'swap_metrics',
        'fields': {
            'swap_total': swap_metrics['total'],
            'swap_used': swap_metrics['used'],
            'swap_free': swap_metrics['free'],
            'swap_percent': swap_metrics['percent'],
        },
        'tags': {
            'hostname': hostname,
        }
    }
    points.append(swap_metric)
    logger.info('SWAP metric prepared')
    logger.debug(swap_metric)

    # Disk metrics
    for disk_name, disk_metrics in disks_metrics.items():
        disk_metric = {
            'measurement': 'disk_metrics',
            'fields': {
                'disk_total_space': disk_metrics['total_space'],
                'disk_used_space': disk_metrics['used_space'],
                'disk_free_space': disk_metrics['free_space'],
            },
            'tags': {
                'hostname': hostname,
                'device': disk_metrics['device'],
                'mountpoint': disk_metrics['mountpoint'],
                'fs': disk_metrics['fs'],
            }
        }
        points.append(disk_metric)
        logger.info(f'Disks metric for {disk_metrics["device"]} prepared')
        logger.debug(disk_metric)

    for interface_name, interface_metrics in net_metrics.items():
        net_metric = {
            'measurement': 'net_interface_metrics',
            'fields': {
                'net_bytes_sent': interface_metrics['bytes_sent'],
                'net_bytes_recv': interface_metrics['bytes_recv'],
                'net_packets_sent': interface_metrics['packets_sent'],
                'net_packets_recv': interface_metrics['packets_recv'],
                'net_errin': interface_metrics['errin'],
                'net_errout': interface_metrics['errout'],
                'net_dropin': interface_metrics['dropin'],
                'net_dropout': interface_metrics['dropout'],
            },
            'tags': {
                'hostname': hostname,
                'interface': interface_name,
            }
        }
        points.append(net_metric)
        logger.info(f'Network metric for {interface_name} prepared')
        logger.debug(net_metric)

    # Docker container metrics
    for container_id, container_metrics in docker_container_metrics.items():
        container_metric = {
            'measurement': 'docker_container_metrics',
            'fields': {
                'container_name': container_metrics['Name'],
                'container_state': container_metrics['State'],
                'container_image': container_metrics['Image'],
                'container_memory_usage': container_metrics['Memory_usage'],
                'container_cpu_total': container_metrics['Cpu_usage_total'],
                'container_cpu_user': container_metrics['Cpu_usage_user'],
                'container_cpu_kernel': container_metrics['Cpu_usage_kernel'],
                'container_rx_bytes': container_metrics['Rx_bytes'],
                'container_tx_bytes': container_metrics['Tx_bytes'],
            },
            'tags': {
                'hostname': hostname,
                'container_id': container_id,
            }
        }
        points.append(container_metric)
        logger.info(f'Docker container metric for {container_id} prepared')
        logger.debug(container_metric)

    # Docker image metrics
    for image_id, image_metrics in docker_image_metrics.items():
        image_metric = {
            'measurement': 'docker_image_metrics',
            'fields': {
                'image_name': image_metrics['Name'],
                'image_size': image_metrics['Size'],
                'image_containers': image_metrics['Containers'],
            },
            'tags': {
                'hostname': hostname,
                'image_id': image_id,
            }
        }
        points.append(image_metric)
        logger.info(f'Docker image metric for {image_id} prepared')
        logger.debug(image_metric)

    # Docker system metrics
    docker_system_metric = {
        'measurement': 'docker_system_metrics',
        'fields': {
            'docker_version': docker_system_metrics['Version'],
            'docker_swarm_node_id': docker_system_metrics['Swarm_node_id'],
            'docker_storage_driver': docker_system_metrics['Storage_driver'],
            'docker_logging_driver': docker_system_metrics['Logging_driver'],
        },
        'tags': {
            'hostname': hostname,
        }
    }
    points.append(docker_system_metric)
    logger.info(f'Docker system metric prepared')
    logger.debug(docker_system_metric)

    try:
        logger.debug(points)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=config.agent_influx_bucket, record=points)
    except Exception as e:
        logger.warning(f"Error while writing to InfluxDB: {e}")
    finally:
        client.close()