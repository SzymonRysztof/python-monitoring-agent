#!/usr/bin/env python3
import logging
from os import getenv
from dotenv import load_dotenv
import errno
import os

logger = logging.getLogger(__name__)

#TODO better config validation
class Config:
    load_dotenv()
    try:
        influx_url = str(getenv('influx_url').strip())
        influx_bucket = str(getenv('influx_bucket').strip())
        influx_org = str(getenv('influx_org').strip())
        influx_token = str(getenv('influx_token').strip())
    except AttributeError as e:
        logger.error('Environment variable not set: '+str(e))  
        raise AttributeError("All environment variables from .env.dist should be present and set")
    
        
    if "" in [influx_url, influx_bucket, influx_org, influx_token]:
        
        
        print(f'Invalid environment variables value '
                     f'\ninflux_bucket: {influx_bucket}'
                     f'\ninflux_org: {influx_org}'
                     f'influx_token: {influx_token}'
                     f'influx_url: {influx_url}'
                    )
        raise ValueError('Environment variables cannot be empty')
