import logging
from log_helper import configure_logger

logger = logging.getLogger("loggin_test")
logger = configure_logger(logger)

testdict = {'key1':'val1'}
teststr = "TEST"

logger.pprintlvl(f"debugtwo message: {testdict}")
logger.customlvl(f"debugone message: {teststr}")
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")