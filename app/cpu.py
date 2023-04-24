#!/usr/bin/env python3 
import os, psutil
import logging
logger = logging.getLogger(__name__)

def get():
    cpu = {}
    
    try:
        temperature = float(os.popen('vcgencmd measure_temp').read().split('=')[1].strip().strip('C').strip('\''))
    except Exception as e:
        temperature = None
        logging.warning(e)
    
    cores = psutil.cpu_count()
    times = psutil.cpu_times()
    frequency = psutil.cpu_freq()
    load = psutil.getloadavg()
    
    tmp = {
        'cpu': {
            'user': times.user,
            'system': times.system,
            'idle': times.idle,
            'iowait': times.iowait,
            'current': frequency.current,
            'max': frequency.max,
            'min': frequency.min,
            '1m': load[0] * cores,
            '5m': load[1] * cores,
            '15m': load[2] * cores,
            'utilization': psutil.cpu_percent(interval=1),
            'temperature': temperature,
            'processors': cores
        }
    }
    
    cpu.update(tmp)
        
    return cpu

def metrics():
    return get()