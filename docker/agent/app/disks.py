#!/usr/bin/env python3
import psutil
import logging

logger = logging.getLogger(__name__)


def get():
    partitions = psutil.disk_partitions()
    disks = {}
    disks_tmp = {}
    tmp = {}
    for part in partitions:
        if part.mountpoint:
            try:
                df = psutil.disk_usage(part.mountpoint)
            except PermissionError as e:
                logger.warning(f'Couldn\'t read filesystem mounted on {part.mountpoint} skipping')
                logger.info(f'{str(e)}')
                continue
            tmp = {
                part.device: {}
            }

            try:
                tmp[part.device]['device'] = part.device
            except Exception as e:
                tmp[part.device]['device'] = None
                logger.warning(f'Error occurred while accessing part.device: {e}')

            try:
                tmp[part.device]['mountpoint'] = part.mountpoint
            except Exception as e:
                tmp[part.device]['mountpoint'] = None
                logger.warning(f'Error occurred while accessing part.mountpoint: {e}')

            try:
                tmp[part.device]['fs'] = part.fstype
            except Exception as e:
                tmp[part.device]['fs'] = None
                logger.warning(f'Error occurred while accessing part.fstype: {e}')

            try:
                tmp[part.device]['total_space'] = df.total
            except Exception as e:
                tmp[part.device]['total_space'] = None
                logger.warning(f'Error occurred while accessing df.total: {e}')

            try:
                tmp[part.device]['used_space'] = df.used
            except Exception as e:
                tmp[part.device]['used_space'] = None
                logger.warning(f'Error occurred while accessing df.used: {e}')

            try:
                tmp[part.device]['free_space'] = df.free
            except Exception as e:
                tmp[part.device]['free_space'] = None
                logger.warning(f'Error occurred while accessing df.free: {e}')

        disks_tmp.update(tmp)
    disks = {'disks': disks_tmp}
    return disks


def metrics():
    return get()
