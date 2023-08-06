# Copyright: 北京物元数界科技有限公司
# Author: 邵芒
# Contact: 微信 stormx

import logging, sys
logging.GREEN = 21
logging.addLevelName(logging.GREEN, "GREEN")
def green(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.GREEN):
        self._log(logging.GREEN, message, args, **kwargs)
logging.Logger.green = green

class CustomFormatter(logging.Formatter):
    grey = "\033[33;1;30m"
    cyan = "\033[33;1;36m"
    yellow = "\033[33;1;33m"
    red = "\033[33;1;31m"
    bold_red = "\033[33;7;31m"
    green = "\033[33;1;32m"
    reset = "\033[0m"
    format = '%(asctime)s: %(message)s'
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: cyan + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
        logging.GREEN: green + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)
    
logger = logging.getLogger("mtnode")
logger.setLevel(logging.DEBUG)
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setFormatter(CustomFormatter())
logger.addHandler(stdout)

if __name__ == '__main__':
    logger.info("This is a test")
    logger.debug("This is a test")
    logger.warning("This is a test")
    logger.error("This is a test")
    logger.critical("This is a test")