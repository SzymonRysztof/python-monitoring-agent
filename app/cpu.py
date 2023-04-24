#!/usr/bin/env python3
import os, psutil
import logging
from time import sleep
logger = logging.getLogger(__name__)


def get():
    #Sleeping here to make sure that CPU frequency is not altered by fact of running this tool
    sleep(5)
    cpu = {}

    cores = psutil.cpu_count()
    times = psutil.cpu_times()
    frequency = psutil.cpu_freq()
    load = psutil.getloadavg()

    cpu = {
        'cpu': {}
    }

    try:
        cpu['cpu']['user'] = times.user
    except Exception as e:
        cpu['cpu']['user'] = None
        logging.exception(f"Error occurred while accessing times.user: {e}")

    try:
        cpu['cpu']['system'] = times.system
    except Exception as e:
        cpu['cpu']['system'] = None
        logging.exception(f"Error occurred while accessing times.system: {e}")

    try:
        cpu['cpu']['idle'] = times.idle
    except Exception as e:
        cpu['cpu']['idle'] = None
        logging.exception(f"Error occurred while accessing times.idle: {e}")

    try:
        cpu['cpu']['iowait'] = times.iowait
    except Exception as e:
        cpu['cpu']['iowait'] = None
        logging.exception(f"Error occurred while accessing times.iowait: {e}")

    try:
        cpu['cpu']['current'] = frequency.current
    except Exception as e:
        cpu['cpu']['current'] = None
        logging.exception(f"Error occurred while accessing frequency.current: {e}")

    try:
        cpu['cpu']['max'] = frequency.max
    except Exception as e:
        cpu['cpu']['max'] = None
        logging.exception(f"Error occurred while accessing frequency.max: {e}")

    try:
        cpu['cpu']['min'] = frequency.min
    except Exception as e:
        cpu['cpu']['min'] = None
        logging.exception(f"Error occurred while accessing frequency.min: {e}")

    try:
        cpu['cpu']['1m'] = load[0] * cores
    except Exception as e:
        cpu['cpu']['1m'] = None
        logging.exception(f"Error occurred while accessing load[0]: {e}")

    try:
        cpu['cpu']['5m'] = load[1] * cores
    except Exception as e:
        cpu['cpu']['5m'] = None
        logging.exception(f"Error occurred while accessing load[1]: {e}")

    try:
        cpu['cpu']['15m'] = load[2] * cores
    except Exception as e:
        cpu['cpu']['15m'] = None
        logging.exception(f"Error occurred while accessing load[2]: {e}")

    try:
        cpu['cpu']['utilization'] = psutil.cpu_percent(interval=1)
    except Exception as e:
        cpu['cpu']['utilization'] = None
        logging.exception(f"Error occurred while accessing psutil.cpu_percent: {e}")

    try:
        cpu['cpu']['temperature'] = float(os.popen('vcgencmd measure_temp').read().split('=')[1].strip().strip('C').strip('\''))
    except Exception as e:
        cpu['cpu']['temperature'] = None
        logging.exception(f"Error occurred while accessing temperature: {e}")

    try:
        cpu['cpu']['processors'] = cores
    except Exception as e:
        cpu['cpu']['processors'] = None
        logging.exception(f"Error occurred while accessing cores: {e}")

    return cpu

def metrics():
    return get()
