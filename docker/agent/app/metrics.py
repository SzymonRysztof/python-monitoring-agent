#!/usr/bin/env python3
import logging

logger = logging.getLogger(__name__)


# Import modules used for fetching metrics
def get_metrics():
    from .disks import metrics as disks
    from .cpu import metrics as cpu
    from .memory import metrics as memory
    from .net_interfaces import metrics as net_interfaces
    from .docker import metrics as docker

    metrics = {}

    # Update metrics dictionary with returned values from sub modules
    metrics.update(disks())
    metrics.update(cpu())
    metrics.update(memory())
    metrics.update(net_interfaces())
    metrics.update(docker())
    return metrics
