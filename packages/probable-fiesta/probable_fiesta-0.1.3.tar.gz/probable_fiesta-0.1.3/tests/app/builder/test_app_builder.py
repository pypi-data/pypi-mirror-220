"""Unit test file for app.builder.app_builder.py."""
from src.probable_fiesta.app.builder import app_builder
from src.probable_fiesta.app.builder import context
from src.probable_fiesta.logger.logging_config import set_logger
from src.probable_fiesta.command.builder.command_factory import CommandFactory
from src.probable_fiesta.command.builder.command_queue import CommandQueue
from src.probable_fiesta.cli.builder.parser import Parser

# Create a logger
from logging import DEBUG
from unittest import TestCase

LOG = set_logger("test_app_builder", DEBUG)


class TestAppBuilderAppBuilder(TestCase):
    def setUp(self):
        self.aB = app_builder.AppBuilder()

    def test_init(self):
        LOG.info("Test init")

        self.aB = app_builder.AppBuilder()
        app = (
            self.aB.name.set_name("app_name")
            .arguments.set_arguments(["--test-app", "test_argument"])
            .args_parser.add_argument("--test-app", type=str, help="test app builder")
            .context.add_context(
                context.Context.Factory().new_context(
                    "test_app",
                    CommandQueue.new(
                        [
                            [
                                CommandFactory.new_command(
                                    "test_app_func", lambda x: x, "repeated"
                                )
                            ]
                        ]
                    ),
                )
            )
            .validate()
            .build()
        )
        print(app)
        self.assertEqual(app.name, "app_name")

    def test_clean_arg_function(self):
        LOG.info("Test clean arg function")
        self.aB = app_builder.AppBuilder()

        test1 = self.aB.arguments.clean_arg_function(["-t", "arg"])
        test2 = self.aB.arguments.clean_arg_function(["--t", "arg"])
        test3 = self.aB.arguments.clean_arg_function(["-t1", "arg1", "-t2", "arg2"])
        test4 = self.aB.arguments.clean_arg_function(["-t", "arg1", "arg2"])
        test5 = self.aB.arguments.clean_arg_function(["-t-t-t", "arg"])

        self.assertEqual(test1, {"t": ["arg"]})
        self.assertEqual(test2, {"t": ["arg"]})
        self.assertEqual(test3, {"t1": ["arg1"], "t2": ["arg2"]})
        self.assertEqual(test4, {"t": ["arg1", "arg2"]})
        self.assertEqual(test5, {"t-t-t": ["arg"]})

    def test_map_short_flags(self):
        LOG.info("Test map short flags")

        # Test 1 argument
        self.aB = app_builder.AppBuilder()
        args = ["-t", "arg"]
        clean_args = self.aB.arguments.clean_arg_function(args)
        p = Parser()
        p.add_argument("-t", type=str, help="test app builder")
        p.parse_args(args)
        test1 = self.aB.arguments.map_short_flags(clean_args, vars(p.get_parsed_args()))
        self.assertEqual(test1, {"t": ["arg"]})

        # Test multiple arguments
        self.aB = app_builder.AppBuilder()
        args = ["-t", "arg1", "arg2"]
        clean_args = self.aB.arguments.clean_arg_function(args)
        p = Parser()
        p.add_argument("-t", type=str, nargs="+", help="test app builder")
        p.parse_args(args)
        test1 = self.aB.arguments.map_short_flags(clean_args, vars(p.get_parsed_args()))
        self.assertEqual(test1, {"t": ["arg1", "arg2"]})

        # Test 1 argument with many dashes
        self.aB = app_builder.AppBuilder()
        args = ["-t3-t2-t1", "arg"]
        clean_args = self.aB.arguments.clean_arg_function(args)
        print(clean_args)
        p = Parser()
        p.add_argument("-t3-t2-t1", type=str, help="test app builder")
        p.parse_args(args)
        test = self.aB.arguments.map_short_flags(clean_args, vars(p.get_parsed_args()))
        self.assertEqual(test, {"t3-t2-t1": ["arg"]})
