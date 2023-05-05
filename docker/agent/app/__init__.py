def main():
    import logging
    from os import getenv
    from sys import stdout
    from dotenv import load_dotenv, find_dotenv
    from config import Logger
    # try:
    #     load_dotenv(find_dotenv())
    # except Exception as e:
    #     pass
    #
    # try:
    #     verbosity = str(getenv('verbosity').strip().upper())
    # except Exception as e:
    #     print(e)
    #     verbosity = 'WARNING'

    # allowed_verbosity = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
    # if verbosity not in allowed_verbosity:
    #     raise ValueError(f'Verbosity must be one of {str(allowed_verbosity)}')
    #
    # verbosities = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, 'NOTSET': 0}
    # logging.basicConfig(handlers=[logging.StreamHandler(stdout)],
    #                     format='%(levelname)s: %(message)s',
    #                     datefmt='%F %A %T',
    #                     level=verbosities[verbosity])
    Logger()
    import main
    main.main()


if __name__ == "__main__":
    main()
