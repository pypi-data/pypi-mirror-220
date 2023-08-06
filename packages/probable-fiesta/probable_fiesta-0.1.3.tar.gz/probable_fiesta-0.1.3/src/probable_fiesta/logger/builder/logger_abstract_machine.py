from abc import ABC
from enum import Enum, auto

from .logger_factory import LoggerFactory


class AbstractLogger(ABC):
    def create_logger(self):
        raise NotImplementedError


class LoggerDefault(AbstractLogger):
    def create_logger(self):
        raise NotImplementedError


class LoggerFlask(AbstractLogger):
    def create_logger(self):
        raise NotImplementedError


class LoggerAbstractFactory(ABC):
    def create_default_logger(self, name, level, fmt, directory):
        raise NotImplementedError

    def create_flask_logger(self, app, name, level, fmt, directory):
        raise NotImplementedError


class DefaultFactory(LoggerAbstractFactory):
    def create_default_logger(self, name, level, fmt, directory):
        # print("Creating default logger")
        logger = LoggerFactory().new_logger_get_logger(name, level, fmt, directory)
        return logger


class FlaskFactory(LoggerAbstractFactory):
    def create_flask_logger(self, app, name, level, fmt, directory):
        # print("Creating flask logger")
        logger = LoggerFactory().new_logger_flask(app, name, level, fmt, directory)
        return logger


class LoggerMachine:
    class Available(Enum):
        DEFAULT = auto()
        FLASK = auto()

    factories = {Available.DEFAULT: DefaultFactory(), Available.FLASK: FlaskFactory()}

    def __str__(self):
        return f"LoggerMachine: Available loggers: {list(self.factories.keys())}"

    def make_logger(
        self, type, app=None, name=None, level=None, fmt=None, directory=None
    ):
        if type in self.factories:
            if type == LoggerMachine.Available.DEFAULT:
                return self.factories[type].create_default_logger(
                    name, level, fmt, directory
                )
            elif type == LoggerMachine.Available.FLASK:
                return self.factories[type].create_flask_logger(
                    app, name, level, fmt, directory
                )
        else:
            print("Invalid logger type")
            return None
