"""Unit test file for config.builder.config.py."""
from src.probable_fiesta.config.builder import config
#from src.probable_fiesta.logger.logging_config import set_logger

#from logging import DEBUG
from unittest import TestCase

# Create a logger
#LOG = set_logger("test_command_builder", DEBUG)


class TestConfig(TestCase):

    def setUp(self):
        self.config = config.Config()

    def test_init(self):
        #LOG.info("Test init")
        self.config = config.Config()
        self.assertEqual(str(self.config), "Config: {'package': {}, 'logger': None, 'variables': {}, 'dotenv': None, 'parsed_dotenv': {}}")

    def test_get_setting_not_loaded(self):
        #LOG.info("Test get_setting()")
        self.config = config.Config()
        self.assertEqual(self.config.get_setting("test"), None)