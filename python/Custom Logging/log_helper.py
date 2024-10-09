"""
Module demonstrating custom logging using python logger
https://docs.python.org/3/library/logging.html
logging.NOTSET 0
logging.DEBUG 10
logging.INFO 20
logging.WARNING 30
logging.ERROR 40
logging.CRITICAL 50
"""

import logging
from lib.config import ConfigSingleton
from pprint import pprint

class LogHelper:

    def addLoggingLevel(levelName, levelNum):
        """
        Based on https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945
        """
        methodName = levelName.lower()

        if hasattr(logging, levelName):
            raise AttributeError(
                "{} already defined in logging module".format(levelName)
            )
        if hasattr(logging, methodName):
            raise AttributeError(
                "{} already defined in logging module".format(methodName)
            )
        if hasattr(logging.getLoggerClass(), methodName):
            raise AttributeError(
                "{} already defined in logger class".format(methodName)
            )

        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)

        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)


class LogFormatter(logging.Formatter):
    """
    Based on https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    """

    LogHelper.addLoggingLevel("CUSTOMLVL", 33)
    LogHelper.addLoggingLevel("PPRINTLVL", 15)

    BRMAGENTA = "\033[95m"
    MAGENTA = "\033[35m"
    WHITE = "\033[97m"
    CYAN = "\033[36m"
    BRGREEN = "\033[92m"
    BRBLUE = "\033[94m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BRYELLOW = "\033[93m"
    RED = "\033[31m"
    BRRED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "%(message)s"
    err_format = "%(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: CYAN + BOLD + format + ENDC,
        logging.PPRINTLVL: pprint(format),
        logging.INFO: BRBLUE + BOLD + format + ENDC,
        logging.WARNING: YELLOW + BOLD + format + ENDC,
        logging.CUSTOMLVL: BRYELLOW + format + ENDC,
        logging.ERROR: RED + BOLD + err_format + ENDC,
        logging.CRITICAL: BRRED + BOLD + err_format + ENDC,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def configure_logger(logger):
    logger.setLevel('DEBUG')

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setFormatter(LogFormatter())
    logger.addHandler(ch)

    return logger