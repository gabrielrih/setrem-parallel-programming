import logging
import logging.config

from src.env import LOG_LEVEL


class Logger:
    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(level=LOG_LEVEL)
        handler = logging.StreamHandler()
        handler.setLevel(LOG_LEVEL)

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d]"
            " - %(message)s"
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
