import logging
from logging.handlers import RotatingFileHandler
from os import path, makedirs

class LoggerFactory(object):
    root_logger = None
    loggers = {}
    file_handler = None
    console_handler = None

    def __init__(self, dir='logs', fname='app.log', log_file_size = 5242880, backups_count = 5) -> None:
        logFormatter = logging.Formatter("%(asctime)s [%(name)s] [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        dest = path.join(dir, fname)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(logFormatter)
        self.root_logger = logging.getLogger(__name__)
        self.root_logger.setLevel(logging.DEBUG)
        self.root_logger.addHandler(self.console_handler)

        try:
            self.file_handler = RotatingFileHandler(dest, maxBytes=log_file_size, backupCount=backups_count)
            self.file_handler.setFormatter(logFormatter)
            if not path.exists(dest):
                self.root_logger.debug(f"Initializing logs folder to: {dest}")
                makedirs(dest)
            self.root_logger.addHandler(self.file_handler)
        except:
            self.root_logger.warning(f"Could not initialize logs folder: {dest}")
            self.file_handler = None




    def instance(self, name, level = logging.DEBUG):
        if name in self.loggers:
            return self.loggers[name]
        else:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(self.console_handler)
            if self.file_handler is not None:
                logger.addHandler(self.file_handler)
            self.loggers[name] = logger
            return logger

    def close(self):
        logging.shutdown()
