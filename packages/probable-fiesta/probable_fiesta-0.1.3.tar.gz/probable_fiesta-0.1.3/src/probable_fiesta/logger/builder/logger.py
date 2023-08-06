"""Logger class."""
import logging


class Logger:
    def __init__(self, name=None, level=None, fmt=None, directory=None):
        # properties
        self.name = name
        self.level = level
        self.fmt = fmt
        self.directory = directory
        # objects
        self.logger = None
        self.file_handler = None

    # Additional Method
    def set_up_logger(self, log_name=None, log_level=None, format=None):
        if log_name is None:
            log_name = self.name
        if log_level is None:
            log_level = self.level
        if format is None:
            format = self.fmt

        self.logger = self.set_logger(log_name, log_level, format)
        return self.logger

    def set_logger(self, log_name, log_level, format):
        logger = logging.getLogger(log_name)

        if log_level is None:
            log_level = logging.INFO
        else:
            log_level = self.parse_level(log_level)

        logger.setLevel(log_level)

        formatter = self.set_formatter_format(format)

        path = f"{self.directory}/{log_name}.log"
        # print(f"Using {path} as the log file")

        fileh = logging.FileHandler(path, "a")
        fileh.setFormatter(formatter)
        logger.addHandler(fileh)

        return logger

    def set_formatter_format(self, option=None):
        options = ["simple", "process", "function", "fun"]
        if option not in options:
            raise ValueError(
                f"Invalid option for formatter format: {option}. Valid options are {options}."
            )

        if option == "simple":
            return logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        if option == "process":
            return logging.Formatter(
                "%(asctime)s %(module)s -> %(process)d -  %(message)s"
            )
        if option == "function":
            return logging.Formatter(
                "%(asctime)s %(module)s %(funcName)s -  %(message)s"
            )
        if option == "fun":
            return FormatterWithEmoji(
                "%(asctime)s %(module)s %(funcName)s -  %(message)s"
            )

    def get_logger(self, name=None, level=None, fmt=None, directory=None):
        if self.logger is None:
            self.set_up_logger(name, level, fmt)
        return self.logger

    # def get_logger(self, #name=None, level=None, fmt=None, directory=None):
    # if name is not None:
    # self.name = name
    # if self.name is None:
    # print("Logger Name not set. Cannot create logger.")
    # return None
    # if level is not None:
    # self.level = level
    # if self.level is None:
    # self.level = self.parse_level(self.level)
    # print("Logger Level: ", self.level)
    # if fmt is not None:
    # self.fmt = fmt
    # if directory is not None:
    # self.directory = directory
    ## create logger
    # _logger = logging.getLogger(self.name)
    # _logger.setLevel(self.level)
    # if self.file_handler is None:
    # self.create_file_handler()
    # _logger.addHandler(self.file_handler)
    # self.logger = _logger
    # return self.logger

    def create_file_handler(self, name=None, level=None, fmt=None, directory=None):
        if name is None:
            name = self.name
            if not name:
                print("Logger name not set. Cannot create file handler.")
                return None
        if level is None:
            level = self.level
        if fmt is None:
            fmt = self.fmt
        if directory is None:
            directory = self.directory
            if not directory:
                directory = "./"  # default directory if not set
        # create file handler
        logger_directory = f"{directory}/{name}.log"
        _file_handler = logging.FileHandler(logger_directory)
        _file_handler.setLevel(self.parse_level(level))
        _file_handler.setFormatter(fmt)
        self.file_handler = _file_handler
        return self.file_handler

    @staticmethod
    def parse_level(level):  # defaults to info
        if level is None:
            return logging.INFO
        if level == "DEBUG":
            return logging.DEBUG
        if level == "INFO":
            return logging.INFO
        if level == "WARNING":
            return logging.WARNING
        if level == "ERROR":
            return logging.ERROR
        if level == "CRITICAL":
            return logging.CRITICAL
        return logging.INFO

    def __str__(self) -> str:
        return f"Logger: {self.__dict__}"

    @staticmethod
    def new(name=None, level=None, fmt=None, directory=None):
        return Logger(name, level, fmt, directory)

    @staticmethod
    def new_get_logger(name=None, level=None, fmt=None, directory=None):
        logger = Logger.new(name, level, fmt, directory)
        return logger.get_logger()

    class Factory:
        @staticmethod
        def new_logger(name=None, level=None, fmt=None, directory=None):
            return Logger.new(name, level, fmt, directory)

        @staticmethod
        def new_file_handler(
            name=None, level=None, fmt=None, directory=None
        ) -> logging.FileHandler:
            logger = Logger.new(name, level, fmt, directory)
            return logger.create_file_handler()

    factory = Factory()


class FormatterWithEmoji(logging.Formatter):
    emoji_mapping = {
        "DEBUG": "🐛",
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "CRITICAL": "🚨",
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.emoji_mapping:
            record.msg = f"{self.emoji_mapping[levelname]} {record.msg}"
        return super().format(record)
