#!/usr/bin/env python3 
import os, psutil
from config import Config
import logging
logger = logging.getLogger(__name__)

def get():
    partitions = psutil.disk_partitions()
    disks = {}
    for part in partitions:
        if part.mountpoint:
            df = psutil.disk_usage(part.mountpoint)
            tmp = {
                part.device: {
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fs": part.fstype,
                    "total_space": df.total,
                    "used_space": df.used,
                    "free_space": df.free
                }
            }
        disks.update(tmp)
    return disks

def metrics():
    return get()