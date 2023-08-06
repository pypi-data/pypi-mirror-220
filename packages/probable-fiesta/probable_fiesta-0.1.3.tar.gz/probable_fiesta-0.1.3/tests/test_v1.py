"""Test file for cli/v1.py."""
from src.probable_fiesta.cli.builder.parser_factory import ParserFactory as PF
from src.probable_fiesta.logger.builder.logger_factory import LoggerFactory as LF

from unittest import TestCase

LOG = LF.new_logger_get_logger("test_v1", "DEBUG")


class TestCliV1(TestCase):


    def test_parse_arguments_short_flags(self):
        """Test parsed arguments."""
        # you can also test long flags but it's redundant.
        #parsed = PF().new_only_args(['--version'])
        #parsed = self.parser.parser.parse_args(['--version'])
        #self.assertEqual(parsed.version, True)
        ## Add more tests here

    def test_parse_arguments_invalid(self):
        test_arguments = '--unknown invalid'
        #self.parser.parse_args(test_arguments.split())
        #parsed = PF().new(test_arguments.split())
        #expected = f"unrecognized arguments: {test_arguments}"
        #self.assertEqual(parsed.error_message, expected)

    def test_parse_arguments_empty(self):
        test_arguments = None
        #parsed = PF().new(test_arguments)
        #expected = "invalid empty arguments"
        #self.assertEqual(parsed, expected)