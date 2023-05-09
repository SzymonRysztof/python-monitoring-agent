#!/usr/bin/env python3
import psutil
import logging

logger = logging.getLogger(__name__)


def get():
    memory = {}
    ram_dict = {
        "ram": {}
    }

    ram = psutil.virtual_memory()

    try:
        ram_dict["ram"]["total"] = ram.total
    except Exception as e:
        ram_dict["ram"]["total"] = None
        logger.warning(f"Error occurred while accessing ram.total: {e}")

    try:
        ram_dict["ram"]["used"] = ram.used
    except Exception as e:
        ram_dict["ram"]["used"] = None
        logger.warning(f"Error occurred while accessing ram.used: {e}")

    try:
        ram_dict["ram"]["free"] = ram.free
    except Exception as e:
        ram_dict["ram"]["free"] = None
        logger.warning(f"Error occurred while accessing ram.free: {e}")

    try:
        ram_dict["ram"]["cached"] = ram.cached
    except Exception as e:
        ram_dict["ram"]["cached"] = None
        logger.warning(f"Error occurred while accessing ram.cached: {e}")

    try:
        ram_dict["ram"]["buffers"] = ram.buffers
    except Exception as e:
        ram_dict["ram"]["buffers"] = None
        logger.warning(f"Error occurred while accessing ram.buffers: {e}")

    try:
        ram_dict["ram"]["percent"] = ram.percent
    except Exception as e:
        ram_dict["ram"]["percent"] = None
        logger.warning(f"Error occurred while accessing ram.percent: {e}")
        memory.update(ram_dict)

    memory.update(ram_dict)

    swap_dict = {
        "swap": {}
    }

    swap = psutil.swap_memory()

    try:
        swap_dict["swap"]["total"] = swap.total
    except Exception as e:
        swap_dict["swap"]["total"] = None
        logger.warning(f"Error occurred while accessing swap.total: {e}")

    try:
        swap_dict["swap"]["used"] = swap.used
    except Exception as e:
        swap_dict["swap"]["used"] = None
        logger.warning(f"Error occurred while accessing swap.used: {e}")

    try:
        swap_dict["swap"]["free"] = swap.free
    except Exception as e:
        swap_dict["swap"]["free"] = None
        logger.warning(f"Error occurred while accessing swap.free: {e}")

    try:
        swap_dict["swap"]["percent"] = swap.percent
    except Exception as e:
        swap_dict["swap"]["percent"] = None
        logger.warning(f"Error occurred while accessing swap.percent: {e}")

    memory.update(swap_dict)

    return memory


def metrics():
    return get()
