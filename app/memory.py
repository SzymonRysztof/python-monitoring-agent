#!/usr/bin/env python3 
import psutil
import logging
logger = logging.getLogger(__name__)

def get():
    memory = {}
    ram = psutil.virtual_memory()
    ram_dict = {
        "ram": {
            "total": ram.total,
            "used": ram.used,
            "free": ram.free,
            "cached": ram.cached,
            "buffers": ram.buffers,
            "percent": ram.percent
        }
    }
    memory.update(ram_dict)

    
    swap = psutil.swap_memory()
    swap_dict = {
        "swap": {
            "total": swap.total,
            "used": swap.used,
            "free": swap.free,
            "percent": swap.percent
        }
    }
    memory.update(swap_dict)
    
    return memory
    
def metrics():
    return get()