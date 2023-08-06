"""Unit test file for command_context_factory.py."""
import unittest
from src.probable_fiesta.app.builder.command_context_factory import (
    CommandContextFactory,
)
from src.probable_fiesta.app.builder.app_builder import AppBuilder
from src.probable_fiesta.command.builder.command_factory import CommandFactory
from src.probable_fiesta.command.builder.command_queue import CommandQueue


class TestCommandContextFactory(unittest.TestCase):
    def setUp(self):
        self.app_builder = AppBuilder()

    def test_command_context_factory(self):
        def sample_function(a, b):
            return str(a + b)

        context_name = "sample_context"
        command_name = "sample_command"
        arg1, arg2 = 1, 2

        # Create a CommandQueue object and add the command
        command_queue = CommandQueue.new(
            [[CommandFactory.new_command(command_name, sample_function, "repeated")]]
        )

        command_context = CommandContextFactory.create_command_context(
            context_name, command_queue, sample_function
        )
        self.app_builder.context.add_context(command_context)

        # Run the created command
        self.app_builder.build().run(context_name)

        # Check the output
        run_history = self.app_builder.build().get_run_history()
        if run_history:
            stdout = self.app_builder.build().get_output()
        else:
            stdout = None

        print("Run history:", run_history)  # Add this print statement for debugging
        print("Actual output:", stdout)  # Add this print statement for debugging

        expected_output = sample_function(arg1, arg2)
        print(
            "Expected output:", expected_output
        )  # Add this print statement for debugging

        self.assertEqual(stdout, expected_output)
