import logging

#create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

#create file handler and set level to error
cf = logging.FileHandler(filename="./logStudy.log", mode="a")
cf.setLevel(logging.ERROR)

#create formatter
formatter = logging.Formatter("%(asctime)s-%(name)s [%(levelname)s] %(message)s")

#add formatter to ch, cf
ch.setFormatter(formatter)
cf.setFormatter(formatter)

#add ch and cf to logger
logger.addHandler(ch)
logger.addHandler(cf)

logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")

if __name__ == "__main__":
    test()
