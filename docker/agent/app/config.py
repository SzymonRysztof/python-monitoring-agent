#!/usr/bin/env python3
import logging
from os import getenv, uname
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


# TODO better config validation
class Config:
    try:
        load_dotenv()
    except Exception as e:
        logging.info("Couldn't locate .env file")

    try:
        influx_url = str(getenv('AGENT_INFLUX_URL').strip())
        influx_bucket = str(getenv('AGENT_INFLUX_BUCKET').strip())
        influx_org = str(getenv('AGENT_INFLUX_ORG').strip())
        influx_token = str(getenv('AGENT_INFLUX_TOKEN').strip())
    except AttributeError as e:
        logger.error(f'Environment variable not set: {str(e)}')
        raise AttributeError(
            'All environment variables from .env.dist should be present and set'
        ) from e

    try:
        hostname = str(getenv('HOSTNAME').strip())
    except Exception as e:
        hostname = uname()[1]
        logger.error(f'Environment variable not set: {str(e)}')

    if hostname == "":
        hostname = uname()[1]

    if "" in [influx_url, influx_bucket, influx_org, influx_token]:
        logging.critical(f'Invalid environment variables value ')
        logging.debug(f'Invalid environment variables value'
                      f'\ninflux_bucket: {influx_bucket}'
                      f'\ninflux_org: {influx_org}'
                      f'\ninflux_token: {influx_token}'
                      f'\ninflux_url: {influx_url}'
                      )
        raise ValueError('Environment variables cannot be empty')
