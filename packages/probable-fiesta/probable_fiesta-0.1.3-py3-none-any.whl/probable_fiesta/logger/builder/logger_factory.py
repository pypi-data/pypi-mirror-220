from .logger import Logger
from ...config.variables import LoggerDef


class LoggerFactory:
    @staticmethod
    def new_logger(name=None, level=None, fmt=None, directory=None):
        return Logger.factory.new_logger(name, level, fmt, directory)

    @staticmethod
    def new_logger_get_logger(name=None, level=None, fmt=None, directory=None):
        return Logger.new_get_logger(name, level, fmt, directory)

    @staticmethod
    def new_logger_default(name=None, level=None, fmt=None, directory=None):
        if not directory:
            directory = LoggerDef.ROOT_DIR + "/logger"
        if not fmt:
            fmt = LoggerDef.FORMAT
        return Logger.new_get_logger(name, level, fmt, directory)

    @staticmethod
    def new_logger_flask(app, name, level, fmt, directory):
        file_handler = Logger.factory.new_file_handler(name, level, fmt, directory)
        app.logger.addHandler(file_handler)
        return app.logger
