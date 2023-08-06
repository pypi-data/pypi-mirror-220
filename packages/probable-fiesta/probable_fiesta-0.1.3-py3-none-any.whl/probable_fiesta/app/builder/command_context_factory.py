"""command_context_factory"""
from .context_factory import ContextFactory


class CommandContextFactory:
    @staticmethod
    def create_command_context(context_name, command_name, function, *args):
        command_context = ContextFactory.new_context_one_new_command(
            context_name, command_name, function, *args
        )
        return command_context
