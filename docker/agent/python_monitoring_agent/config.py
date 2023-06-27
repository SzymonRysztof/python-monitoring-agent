#!/usr/bin/env python3
import logging, re, yaml
import os
from sys import stdout, exit

logger = logging.getLogger(__name__)


class Config:

    def __init__(self):
        self.default_polling_rate = 60
        self.agent_hostname = ''
        if os.getenv('AGENT_DOCKER') is not None:
            try:
                self.agent_influx_url = str(os.getenv('AGENT_INFLUX_URL').strip())
                self.agent_influx_bucket = str(os.getenv('AGENT_INFLUX_BUCKET').strip())
                self.agent_influx_org = str(os.getenv('AGENT_INFLUX_ORG').strip())
                self.agent_influx_token = str(os.getenv('AGENT_INFLUX_TOKEN').strip())
                self.agent_verbosity = str(os.getenv('AGENT_VERBOSITY').strip())
                self.agent_hostname = str(os.getenv('AGENT_HOSTNAME')).strip()
                self.agent_polling_rate = int(os.getenv('AGENT_POLLING_RATE'))
            except AttributeError as e:
                logger.error(f'Environment variable not set: {str(e)}')
                raise AttributeError(
                    'All environment variables from .env.dist should be present and set'
                ) from e
            except TypeError as e:
                logger.error(f'Couldn\'t cast one of environment variables: {str(e)}')
            logger.debug('Found docker environment, loaded config from environment')

        else:
            if os.getenv("XDG_CONFIG_HOME"):
                path = f'{os.getenv("XDG_CONFIG_HOME")}/python-monitoring-agent'
            else:
                home = os.path.expanduser('~')
                path = f'{home}/.config/python-monitoring-agent'
            file_name = 'config.yaml'
            config_file = f'{path}/{file_name}'
            if os.path.isfile(config_file):
                try:
                    with open(config_file, 'r') as f:
                        config_yaml = yaml.safe_load(f)
                except Exception as e:
                    logger.critical(f'Couldn\'t open config file {config_file}/ {str(e)}')

                self.agent_influx_url = config_yaml['agent']['INFLUX_URL']
                self.agent_influx_bucket = config_yaml['agent']['INFLUX_BUCKET']
                self.agent_influx_org = config_yaml['agent']['INFLUX_ORG']
                self.agent_influx_token = config_yaml['agent']['INFLUX_TOKEN']
                self.agent_verbosity = config_yaml['agent']['VERBOSITY']
                self.agent_hostname = config_yaml['agent']['HOSTNAME']
                try:
                    self.agent_polling_rate = int(config_yaml['agent']['POLLING_RATE'])
                except ValueError:
                    self.agent_polling_rate = self.default_polling_rate
                    logger.warning(
                        f'Couldn\'t cast agent_polling_rate to int, defaulting to {self.default_polling_rate}')

            else:
                logger.critical(f'Couldn\'t find config file {config_file}. Writing default one')
                config_example = {
                    'agent': {
                        'INFLUX_URL': 'http://influxdb:8086',
                        'INFLUX_BUCKET': 'some_bucket',
                        'INFLUX_ORG': 'some_org',
                        'INFLUX_TOKEN': 'some_token',
                        'VERBOSITY': 'CRITICAL',
                        'HOSTNAME': 'hostname',
                        'POLLING_RATE': 60
                    }}
                try:
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(config_file, 'a+') as f:
                        yaml.dump(config_example, f)
                except Exception as e:
                    logger.critical(f'Couldn\'t write config file to {config_file}. {str(e)}')
                exit(1)

        if self.agent_hostname == '' or None:
            self.agent_hostname = os.uname()[1]
        else:
            self.agent_hostname = self.agent_hostname.strip()

        if '' in [self.agent_influx_url, self.agent_influx_bucket, self.agent_influx_org, self.agent_influx_token]:
            logger.critical(f'Invalid environment variables value ')
            raise ValueError('Environment variables cannot be empty')

        logger.debug(f'Configuration options:'
                     f'\ninflux_bucket: {self.agent_influx_bucket}'
                     f'\ninflux_org: {self.agent_influx_org}'
                     f'\ninflux_token: {self.agent_influx_token[:5]}********{self.agent_influx_token[-5:]}'
                     f'\ninflux_url: {self.agent_influx_url}'
                     f'\nagent_verbosity: {self.agent_verbosity}'
                     f'\nagent_hostname: {self.agent_hostname}'
                     )

        # config = {
        #     'INFLUX_URL': self.agent_influx_url,
        #     'INFLUX_BUCKET': self.agent_influx_bucket,
        #     'INFLUX_ORG': self.agent_influx_org,
        #     'INFLUX_TOKEN': self.agent_influx_token,
        #     'VERBOSITY': self.agent_verbosity,
        #     'HOSTNAME': self.agent_hostname,
        #     'AGENT_POLLING_RATE': self.agent_polling_rate
        # }

    def get_config(self):
        return self


class Logger:
    def __init__(self):
        self.config = Config()

        allowed_verbosity = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
        if self.config.agent_verbosity not in allowed_verbosity:
            raise ValueError(f'Verbosity must be one of {str(allowed_verbosity)}')

        verbosities = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
        logging.basicConfig(handlers=[logging.StreamHandler(stdout)],
                            format='%(levelname)s: %(message)s',
                            datefmt='%F %A %T',
                            level=verbosities[self.config.agent_verbosity])
