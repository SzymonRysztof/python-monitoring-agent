#!/usr/bin/env python3
import logging

logger = logging.getLogger(__name__)


def main():
    import os, json, metrics, time, sys, influx_writer
    from config import Config
    config = Config()

    # Main loop
    while True:
        local_metrics = metrics.get_metrics()
        logger.debug("Values: " + json.dumps(local_metrics, indent=4))
        influx_writer.main(data=local_metrics)
        time.sleep(config.agent_polling_rate)
