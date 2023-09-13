import logging


class ErrorFormatter(logging.Formatter):
    red = "\x1b[31;20m"
    reset = "\x1b[0m"
    format = "%(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: "DotenvManager " + format,
        logging.INFO: "DotenvManager " + format,
        logging.WARNING: "DotenvManager " + format,
        logging.ERROR: "DotenvManager \x1b[31;20m" + format + "\x1b[0m",
        logging.CRITICAL: "DotenvManager \x1b[31;20m" + format + "\x1b[0m",
    }

    def format(self, record):
        return logging.Formatter(self.FORMATS.get(record.levelno)).format(record)


logger = logging.getLogger()
ch = logging.StreamHandler()
ch.setFormatter(ErrorFormatter())
logger.addHandler(ch)
