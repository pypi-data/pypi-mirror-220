"""Unit test file for main_app.py."""
from src.probable_fiesta.app import main as main_app
from src.probable_fiesta.app.builder.app_builder import AppBuilder
from src.probable_fiesta.command.builder import command
from src.probable_fiesta.logger.builder.logger_factory import LoggerFactory
from src.probable_fiesta.__about__ import __version__
from src.probable_fiesta.config.variables import PackageDef, VariablesDef
from src.probable_fiesta.app.builder.context_factory import ContextFactory

from unittest import TestCase

# Create a logger if needed for testing cases
LOG_TEST = LoggerFactory.new_logger_get_logger("test_main_app", "DEBUG")


class TestMainApp(TestCase):
    def setUp(self):
        self.app_builder = AppBuilder()

    # Health-check function test - get current version
    def test_function_get_version(self):
        LOG_TEST.info("Test function get_version()")
        # This should never fail :)
        expected = f"{PackageDef.NAME} v.{VariablesDef.VERSION}"
        self.assertEqual(main_app.get_version(), expected)

    def test_create_command_function_version(self):
        c = command.Command("version test", main_app.get_version, None)
        co = ContextFactory.new_context_one_command("version test", c)
        app = self.app_builder.context.add_context(co).build()
        app.run("version test")
        stdout = app.get_run_history()
        # LOG.debug(stdout)
        expected = f"{PackageDef.NAME} v.{VariablesDef.VERSION}"
        self.assertEqual(stdout, expected)

    def test_argument(self):
        arg = "--version"
        expected = f"{PackageDef.NAME} v.{VariablesDef.VERSION}"
        self.assertEqual(main_app.main([arg]), expected)

    def test_argument_invalid(self):
        arg = "--invalid"
        expected = f"unrecognized arguments: {arg}"
        self.assertEqual(main_app.main([arg]), expected)

    @staticmethod
    def add_one(x):
        return x + 1

    @staticmethod
    def add_two(x):
        return x + 2

    def test_pipe_mode(self):
        LOG_TEST.info("Test pipe mode")

        c1 = command.Command("add_one", TestMainApp.add_one, 1)
        c2 = command.Command("add_two", TestMainApp.add_two, 2)

        co = ContextFactory.new_context("pipe_mode_test")
        co.command_queue.add_command(c1).add_command(c2)

        app = self.app_builder.context.add_context(co).build()
        app.run("pipe_mode_test")

        stdout = app.get_run_history()
        expected = [2, 4]
        self.assertEqual(stdout, expected)
