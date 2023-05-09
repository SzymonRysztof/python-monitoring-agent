def start():
    from .config import Logger
    Logger()
    from .main import main
    main()


if __name__ == "__main__":
    start()
