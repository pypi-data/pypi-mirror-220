from .logger import Logger
from .logger import LoggerFactory


class LoggerBuilder:
    def __init__(self, logger=None):
        if logger is None:
            self.logger = Logger.factory.new_logger()
        else:
            self.logger = logger

    def __str__(self):
        return f"LoggerBuilder: {self.__dict__}"

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    def build(self):
        return self.logger


class LoggerBuilderLogger(LoggerBuilder):
    def __init__(self, logger):
        super().__init__(logger)

    def get_logger_flask_application(
        self,
        application,
        name=None,
        level=None,
        fmt=None,
        directory=None,
        filename=None,
    ):
        _file_handler = Logger.factory.new_file_handler(name, level, fmt, directory)
        application.logger.addHandler(_file_handler)
        return application

    def get_logger_default(
        self, name=None, level=None, fmt=None, directory=None, filename=None
    ):
        print("Getting default logger")
        self.logger = LoggerFactory.new_logger_default(name, level, fmt, directory)
        return self
