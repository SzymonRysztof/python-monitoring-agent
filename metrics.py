#!/usr/bin/env python3 
import os, psutil
from config import Config
import logging
logger = logging.getLogger(__name__)


# Import modules used for fetching metrics
import disks, cpu, memory

metrics = {}

# Update metrics dictionary with returned values from sub modules
metrics.update(disks.metrics())
metrics.update(cpu.metrics())
metrics.update(memory.metrics())
