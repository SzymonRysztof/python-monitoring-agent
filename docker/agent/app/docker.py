#!/usr/bin/env python3
import subprocess
import logging
import json
import re
import socket
from os import stat

logger = logging.getLogger(__name__)


def convert(value: str):
    try:
        number, unit = re.split(r'([0-9.]+)', value.strip())[1:]
    except ValueError as e:
        logger.warning(f'Couldn\'t convert: {e} to Bytes')
        return None
    try:
        number = float(number)
    except ValueError:
        logger.warning(f'Can\'t cast {number} to float')
        return None

    if unit == 'B':
        return int(number)

    units = {'KB': 1, 'MB': 2, 'GB': 3, 'TB': 4, 'PB': 5}
    return int(number * (1000 ** units[unit.upper()]))


# Function takes query as argument and returns python object containing response, or none
# if docker socket is not available
def docker_socket(query: str):
    request = f'GET /v1.25{query} HTTP/1.1\r\nHost: localhost\r\n\r\n'.encode()
    socket_path = '/var/run/docker.sock'
    if not stat(socket_path):
        return None
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(socket_path)
        sock.sendall(request)

        response = b''
        while True:
            chunk = sock.recv(4096)
            response += chunk
            if len(chunk) < 4096:
                break
        headers, _, body = response.partition(b'\r\n\r\n')
        body = body.decode('utf-8')
        if body[0] not in ['{', '[']:
            body = body.split('\n')[1]

        body = json.loads(body)
        # Make sure that docker socket response is as expected
        if 'message' in body and body['message'] == 'page not found':
            logger.error(f'Invalid response from docker API')
            logger.info(f'API response: {body["message"]}')
            return None

        return body
    finally:
        sock.close()


def get_containers():
    containers_json = docker_socket('/containers/json?all=true')
    if containers_json is None:
        return None
    containers_tmp = {}
    for container in containers_json:
        id = container['Id']
        tmp = {
            id: {}
        }

        stats = docker_socket(f"/containers/{id}/stats?stream=false")

        try:
            tmp[id]['Name'] = container['Names'][0]
        except Exception as e:
            tmp[id]['Name'] = None
            logger.warning(f'Error occurred while accessing container\'s name: {e}')
        try:
            tmp[id]['State'] = container['State']
        except Exception as e:
            tmp[id]['State'] = None
            logger.warning(f'Error occurred while accessing container\'s state: {e}')
        try:
            tmp[id]['Image'] = container['Image']
        except Exception as e:
            tmp[id]['Image'] = None
            logger.warning(f'Error occurred while accessing container\'s image name: {e}')
        try:
            tmp[id]['Memory_usage'] = stats['memory_stats']['usage']
        except Exception as e:
            tmp[id]['Memory_usage'] = None
            logger.warning(f'Error occurred while accessing container\'s memory usage: {e}')
        try:
            tmp[id]['Cpu_usage_total'] = stats['cpu_stats']['cpu_usage']['total_usage']
        except Exception as e:
            tmp[id]['Cpu_usage_total'] = None
            logger.warning(f'Error occurred while accessing container\'s CPU usage: {e}')
        try:
            tmp[id]['Cpu_usage_user'] = stats['cpu_stats']['cpu_usage']['usage_in_usermode']
        except Exception as e:
            tmp[id]['Cpu_usage_user'] = None
            logger.warning(f'Error occurred while accessing container\'s CPU usermode usage: {e}')
        try:
            tmp[id]['Cpu_usage_kernel'] = stats['cpu_stats']['cpu_usage']['usage_in_kernelmode']
        except Exception as e:
            tmp[id]['Cpu_usage_kernel'] = None
            logger.warning(f'Error occurred while accessing container\'s CPU kernelmode usage: {e}')

        rx_bytes = 0
        tx_bytes = 0
        try:
            for interface in stats['networks']:
                rx_bytes += stats['networks'][interface]['rx_bytes']
                tx_bytes += stats['networks'][interface]['tx_bytes']
        except:
            pass

        try:
            tmp[id]['Rx_bytes'] = rx_bytes
        except Exception as e:
            tmp[id]['Rx_bytes'] = None
            logger.warning(f'Error occurred while accessing container\'s received bytes: {e}')
        try:
            tmp[id]['Tx_bytes'] = tx_bytes
        except Exception as e:
            tmp[id]['Tx_bytes'] = None
            logger.warning(f'Error occurred while accessing container\'s transferred bytes: {e}')

        containers_tmp.update(tmp)
    containers = {'containers': containers_tmp}

    return containers


def get_images():
    images = docker_socket("/images/json")
    images_tmp = {}
    for image in images:
        id = image['Id']
        tmp = {
            id: {}
        }

        try:
            tmp[id]['Name'] = image['RepoTags'][0]
        except Exception as e:
            tmp[id]['Name'] = None
            logger.warning(f'Error occurred while accessing image\'s name: {e}')
        try:
            tmp[id]['Size'] = image['Size']
        except Exception as e:
            tmp[id]['Size'] = None
            logger.warning(f'Error occurred while accessing image\'s size: {e}')
        try:
            if image['Containers'] > 0:
                tmp[id]['Containers'] = image['Containers']
            else:
                tmp[id]['Containers'] = 0
        except Exception as e:
            tmp[id]['Containers'] = None
            logger.warning(f'Error occurred while accessing number of container associated with image: {e}')
            logger.debug(f'Image id: {id}')

        images_tmp.update(tmp)
    images = {'images': images_tmp}
    return images


def get_system():
    system = docker_socket("/info")
    system_tmp = {}

    try:
        system_tmp['Version'] = system['ServerVersion']
    except Exception as e:
        system_tmp['Version'] = None
        logger.warning(f'Error occurred while accessing system version: {e}')
    try:
        if system['Swarm']['NodeID'] == "":
            system_tmp['Swarm_node_id'] = None
        else:
            system_tmp['Swarm_node_id'] = system['Swarm']['NodeID']
    except Exception as e:
        system_tmp['Version'] = None
        logger.warning(f'Error occurred while accessing swarm node id: {e}')
    try:
        system_tmp['Storage_driver'] = system['Driver']
    except Exception as e:
        system_tmp['Storage_driver'] = None
        logger.warning(f'Error occurred while accessing storage driver: {e}')
    try:
        system_tmp['Logging_driver'] = system['LoggingDriver']
    except Exception as e:
        system_tmp['Logging_driver'] = None
        logger.warning(f'Error occurred while accessing logging driver: {e}')

    system = {'system': system_tmp}

    return system


# In the future, it may be wise to use docker sdk for python, bot for now, there is no reason to create additional
# dependency for user


def get():
    containers = get_containers()
    images = get_images()
    system = get_system()
    tmp = {}
    tmp.update(containers)
    tmp.update(images)
    tmp.update(system)
    docker = {
        'docker': tmp
    }
    return docker


def metrics():
    return get()


