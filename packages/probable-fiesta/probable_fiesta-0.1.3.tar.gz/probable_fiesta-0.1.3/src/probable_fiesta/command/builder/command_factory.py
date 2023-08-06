"""Command Factory class."""
from .command import Command

class CommandFactory:
    @staticmethod
    def new_command_without_args(name, function, args=None):
        return Command(name, function, *args)

    @staticmethod
    def new_command(name, function, *args):
        return Command.Factory.new_command(name, function, *args)

    @staticmethod
    def new_command_empty():
        return Command(None, None, None)