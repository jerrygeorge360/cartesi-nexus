import os
from cartesi_nexus.logger import setup_logging


def test_logging():
    # Setting teh environment variable
    os.environ['LOG_LEVEL'] = 'DEBUG'

    logger = setup_logging()

    # Log messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


if __name__ == "__main__":
    test_logging()
