"""App context class."""
from ...command.builder.command_queue import CommandQueue


class Context:
    def __init__(self, name=None, command_queue=None):
        self.name = name
        if command_queue is None:
            self.command_queue = CommandQueue()
        else:
            self.command_queue = command_queue

    def __str__(self):
        return f"Context: {self.__dict__}"

    @staticmethod
    def new_context(name=None, command_queue=None):
        return Context(name, command_queue)

    class Factory:
        @staticmethod
        def new_context(name=None, command_queue=None):
            return Context(name, command_queue)

    factory = Factory()
