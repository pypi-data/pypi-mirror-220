import sys
sys.path.append("..")
from zq_tools import logger

if __name__ == '__main__':
    logger.setLevel(logger.DEBUG)
    logger.add_log_file("demo.log", logger.DEBUG)
    logger.info("hello")
    logger.debug("debug msg")
    logger.info("info msg")
