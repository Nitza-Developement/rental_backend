import logging


__logger = logging.getLogger("api")


def log_error(message: str):
    __logger.error(message)
