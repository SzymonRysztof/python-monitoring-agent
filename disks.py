#!/usr/bin/env python3 
import psutil
import logging
logger = logging.getLogger(__name__)

def get():
    partitions = psutil.disk_partitions()
    disks = {}
    disks_tmp = {}
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
        disks_tmp.update(tmp)
    disks = {"disks": disks_tmp}
    return disks

def metrics():
    return get()