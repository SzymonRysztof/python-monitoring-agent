#!/usr/bin/env python3
import logging

logger = logging.getLogger(__name__)


def main():
    import os, json, time, sys
    from .influx_writer import main as influx_writer
    from .config import Config
    from .metrics import get_metrics
    config = Config()

    # Main loop
    while True:
        local_metrics = get_metrics()
        logger.debug("Values: " + json.dumps(local_metrics, indent=4))
        influx_writer(data=local_metrics)
        time.sleep(config.agent_polling_rate)
