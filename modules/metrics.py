#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)


# Import modules used for fetching metrics
import disks, cpu, memory, net_interfaces

metrics = {}

# Update metrics dictionary with returned values from sub modules
metrics.update(disks.metrics())
metrics.update(cpu.metrics())
metrics.update(memory.metrics())
metrics.update(net_interfaces.metrics())
