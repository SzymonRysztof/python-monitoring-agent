#!/usr/bin/env python3
import subprocess
import logging
import json
import re
import math

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

    if unit == "B":
        return int(number)

    units = {'KB': 1, 'MB': 2, 'GB': 3, 'TB': 4, 'PB': 5}
    return int(number * (1000 ** units[unit.upper()]))


# In the future, it may be wise to use docker sdk for python, bot for now, there is no reason to create additional
# dependency for user
def get():
    docker = {'containers': {},
              'images': {},
              'system': {}
              }
    tmp = {}

    # Containers
    cmd = 'docker ps -a --format ' \
          '\'{"ID":"{{ .ID }}", "Image": "{{ .Image }}","Status":"{{ .Status }}", "Name":"{{ .Names }}"}\' '
    containers = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')
    if len(containers) > 0:
        tmp['exited'] = 0
        tmp['created'] = 0
        tmp['running'] = 0
        tmp['exited_n'] = ""
        tmp['created_n'] = ""
        tmp['running_n'] = ""
        for container in containers:
            container_tmp = json.loads(container)
            status = container_tmp['Status'].lower()
            if 'exited' in status:
                tmp['exited'] += 1
                tmp['exited_n'] += container_tmp['Name'] + ','
            elif 'created' in status:
                tmp['created'] += 1
                tmp['created_n'] += container_tmp['Name'] + ','
            elif 'up' in status:
                tmp['running'] += 1
                tmp['running_n'] += json.dumps(container_tmp, indent=4)
        tmp['containers_count'] = len(containers)
    containers_tmp = tmp
    tmp = {}

    # Images
    cmd = 'docker image ls --format \'{"Image_ID":"{{ .ID }}"}\''
    images = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')
    tmp['images_count'] = len(images)
    images_tmp = tmp
    tmp = {}

    # System
    cmd = 'docker system df --format \'{"Type": "{{ .Type }}", "Size":"{{ .Size }}"}\''
    system_df = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')
    tmp['Size'] = 0
    for line in system_df:
        line_tmp = json.loads(line)
        tmp['Size'] += convert(line_tmp['Size'])
    cmd = 'docker --version'
    version = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    version = re.findall(r'[0-9]+.[0-9]+.[0-9]+', version)[0]
    system_tmp = {
        'used': tmp['Size'],
        'version': version
    }

    docker = {'docker':
        {
            'docker_containers': containers_tmp,
            'docker_images': images_tmp,
            'docker_system': system_tmp
        }}

    return docker


def metrics():
    return get()
