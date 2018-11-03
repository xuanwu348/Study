import logging
from util.log_module import logger

logger.name = __name__
print(dir(logger))


def test():
    logger.error("other module error message")
    logger.info("other module info message")

if __name__ == "__main__":
    test()
