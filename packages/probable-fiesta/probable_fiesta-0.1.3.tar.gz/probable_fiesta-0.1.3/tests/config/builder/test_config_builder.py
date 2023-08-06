"""Unit test file for config.builder.config_builder.py."""
from src.probable_fiesta.config.builder import config_builder
#from src.probable_fiesta.logger.logging_config import set_logger

#from logging import DEBUG
from unittest import TestCase

# Create a logger
#LOG = set_logger("test_command_builder", DEBUG)


class TestConfig(TestCase):

    def setUp(self):
        self.cB = config_builder.ConfigBuilder()

    def test_init(self):
        #LOG.info("Test init")
        self.cB = config_builder.ConfigBuilder()
        self.assertEqual(str(self.cB), "ConfigBuilder: {'package': {}, 'logger': None, 'variables': {}, 'dotenv': None, 'parsed_dotenv': {}}")

    def test_package_property(self):
        self.cB = config_builder.ConfigBuilder()

        def test_set_package_name():
            # test package name
            self.cB.package.set_package_name("test")
            self.assertEqual(str(self.cB), "ConfigBuilder: {'package': {'name': 'test'}, 'logger': None, 'variables': {}, 'dotenv': None, 'parsed_dotenv': {}}")
        def test_set_root_dir():
            # test root dir
            self.cB.package.set_root_dir("test")
            self.assertEqual(str(self.cB), "ConfigBuilder: {'package': {'name': 'test', 'root_directory': 'test'}, 'logger': None, 'variables': {}, 'dotenv': None, 'parsed_dotenv': {}}")

        test_set_package_name()
        test_set_root_dir()

    def test_logger_property(self):
        self.cB = config_builder.ConfigBuilder()

        def test_set_logger_level():
            # test logger level
            self.cB.logger.set_logger_level("test")
            self.assertEqual(str(self.cB), "ConfigBuilder: {'package': {}, 'logger': 'test', 'variables': {}, 'dotenv': None, 'parsed_dotenv': {}}")
        def test_set_logger_dir():
            # test logger dir
            self.cB.logger.set_logger_dir("test")
            self.assertEqual(str(self.cB), "ConfigBuilder: {'package': {}, 'logger': 'test', 'variables': {}, 'dotenv': None, 'parsed_dotenv': {}}")
        def test_set_logger_format():
            # test logger format
            self.cB.logger.set_logger_format("test")
            self.assertEqual(str(self.cB), "ConfigBuilder: {'package': {}, 'logger': 'test', 'variables': {}, 'dotenv': None, 'parsed_dotenv': {}}")
        def test_set_logger():
            # test set logger 
            self.cB.logger.set_logger("test")
            self.assertEqual(str(self.cB), "ConfigBuilder: {'package': {}, 'logger': 'test', 'variables': {}, 'dotenv': None, 'parsed_dotenv': {}}")
        def test_set_new_logger():
            # test set new logger
            self.cB.logger.set_new_logger("test", "test", "test")
            self.assertEqual(str(self.cB.build().logger), "Logger: {'name': 'test', 'level': 'test', 'fmt': 'test', 'directory': None, 'logger': None, 'file_handler': None}")
        test_set_logger_level()
        test_set_logger_dir()
        test_set_logger_format()
        test_set_logger()
        test_set_new_logger()
