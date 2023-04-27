#!/usr/bin/env python3


def main():
    import logging, os, json, metrics, time, sys, influx_writer
    from dotenv import load_dotenv
    load_dotenv()

    try:
        verbosity = str(os.getenv('verbosity').strip().upper())
    except Exception as e:
        print(e)
        verbosity = 'WARNING'

    allowed_verbosity = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
    if verbosity not in allowed_verbosity:
        raise ValueError(f'Verbosity must be one of {str(allowed_verbosity)}')

    verbosities = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, 'NOTSET': 0}
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)],
                        format='%(levelname)s: %(message)s',
                        datefmt='%F %A %T',
                        level=verbosities[verbosity])

    try:
        pooling_rate = int(os.getenv('pooling_rate').strip().upper())
    except Exception as e:
        pooling_rate = 60
        logging.info('Polling rate not set, defaulting to 60 seconds')

    # Main loop
    while True:
        local_metrics = metrics.get_metrics()
        logging.debug("Values: " + json.dumps(local_metrics, indent=4))
        influx_writer.main(data=local_metrics)
        time.sleep(pooling_rate)


if __name__ == '__main__':
    main()
