import logging
import sys
import threading


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Use singleton pattern to ensure a unique gloabl logger
        """
        if cls._instance is None:
            cls._lock.acquire()
            if cls._instance is None:
                try:
                    logger = logging.getLogger(__name__)
                    logger.setLevel(logging.DEBUG)
                    logger_handler = logging.StreamHandler(sys.stdout)
                    logger_formater = logging.Formatter("%(levelname)s\t%(message)s")
                    logger_handler.setFormatter(logger_formater)
                    logger.addHandler(logger_handler)
                    cls._instance = logger
                finally:
                    cls._lock.release()
        return cls._instance
