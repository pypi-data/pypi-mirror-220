import logging
import datetime
import configparser
import os


class Logger(object):

    def __init__(self, config: configparser.ConfigParser) -> None:
        self.config = config

        logging.basicConfig(
            level=logging.INFO,
            filename=os.path.join(
                self.config['Logging']['logging_path'],
                datetime.datetime.now().strftime('%d-%m-%Y, %H-%M-%S') + '.log',
            ),
            filemode="w",
            format="%(asctime)s [%(levelname)s]: %(message)s"
        )

    @staticmethod
    def info(message) -> None:
        logging.info(msg=message)

    @staticmethod
    def warning(message) -> None:
        logging.warning(msg=message)

    @staticmethod
    def critical(message) -> None:
        logging.critical(msg=message)

    @staticmethod
    def error(message) -> None:
        logging.error(msg=message)
        exit(-1)

    __call__ = info
