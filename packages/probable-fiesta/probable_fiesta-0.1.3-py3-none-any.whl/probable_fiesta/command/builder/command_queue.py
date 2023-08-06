"""Command Queue class."""
from .command_factory import CommandFactory
from .command import Command

from ...logger.builder.logger_abstract_machine import LoggerMachine

machine = LoggerMachine()
SYSTEM_LOG = machine.make_logger(
    type=LoggerMachine.Available.DEFAULT,
    name="system",
    level="INFO",
    fmt="simple",
    directory="logs",
)


class CommandQueue:
    def __init__(self):
        self.queue = []
        self.history = []
        self.length = 0
        self.output = None  # output of the last executed command

    def add_command(self, command):
        if command is not None:
            self.queue.append(command)
            self.length += 1
        return self

    def add_new_command(self, name, function, *args):
        c = CommandFactory().new_command(name, function, *args)
        if c is not None:
            self.queue.append(c)
            self.length += 1
        return self

    def remove(self, command):
        removed = self.queue.remove(command)
        if removed:
            self.length -= 1
        return self

    def clear(self):
        self.queue = []
        self.length = 0
        return self

    def run_command(self, command, input_data=None):
        self.length -= 1
        result = command.invoke(input_data)
        self.history.append(result)
        self.output = result
        return result

    def run_all(self):
        if self.length <= 0:
            return self
        else:
            previous_result = None
            while self.queue:
                command = self.queue.pop(0)
                previous_result = self.run_command(command, previous_result)
            return self

    def get_history(self):
        "Get history and clears it."
        if len(self.history) <= 0:
            return None
        elif len(self.history) == 1:
            return self.history.pop()
        else:
            temp = self.history
            self.history = []
            return temp

    def show(self):
        return self.queue

    def __str__(self):
        return f"CommandQueue: loaded commands: {self.length} executed commands: {self.history} "

    def print_queue(self):
        for c in self.queue:
            print(c)

    @staticmethod
    def new_empty():
        return CommandQueue()

    @staticmethod
    def new(queue):
        command_queue = CommandQueue()
        if queue is not None:
            if isinstance(queue, list):
                for command in queue:
                    if not isinstance(command, Command):
                        SYSTEM_LOG.error("Invalid command type: %s", type(command))
                    else:
                        command_queue.add_command(command)
                        SYSTEM_LOG.debug("Added command: ", command)
            elif isinstance(queue, CommandQueue):
                command_queue = queue
            elif isinstance(queue, Command):
                # Create a new CommandQueue with a single Command
                command_queue.add_command(queue)
            else:
                SYSTEM_LOG.error("Invalid queue type: %s", type(queue))
        else:
            SYSTEM_LOG.warning("Creating empty queue: %s", queue)
        return command_queue

    def get_output(self):
        # Return the output of the last executed command
        return self.output

    class Factory:
        @staticmethod
        def new_command_queue(command_or_queue):
            return CommandQueue().new(command_or_queue)

    factory = Factory()
