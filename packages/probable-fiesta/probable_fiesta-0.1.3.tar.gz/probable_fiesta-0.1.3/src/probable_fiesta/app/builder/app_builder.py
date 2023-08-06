"""App builder module."""
from ...cli.builder.parser import Parser
from .context_holder import ContextHolder

from ...logger.builder.logger_abstract_machine import LoggerMachine

machine = LoggerMachine()
SYSTEM_LOG = machine.make_logger(
    type=LoggerMachine.Available.DEFAULT,
    name="system",
    level="INFO",
    fmt="simple",
    directory="logs",
)


class App:
    def __init__(self):
        # properties
        self.name = None
        self.args_parser = None
        self.arguments = None
        self.config = None
        self.context = None  # context_holder
        # internal properties
        self.valid = False
        self.error = None
        self.run_history = []
        self.cleaned_args = {}
        self.executables = []  # commands to be run from args
        self.output = None

    def __str__(self):
        return f"App: {self.__dict__}"

    def validate(self):
        local_valid = True

        # validate arguments
        if self.arguments is None:
            print("validate fail: App arguments are empty")
            local_valid = False

        # validate args_parser
        if self.args_parser is not None:
            if not self.args_parser.validate(self.arguments):
                print("App args_parser is not valid")
                self.valid = False

        # validate context
        if self.context is not None:
            if not self.context.validate(self.args_parser.get_parsed_args()):
                print("App context is not valid")
                local_valid = False

        # validate executables
        if self.executables is not None:
            for e in self.executables:
                if e not in self.args_parser.get_parsed_args():
                    print("App executable not valid: ", e)
                    self.executables.remove(e)
            if len(self.executables) == 0:
                print("App executables are not valid")
                local_valid = False

        # validate short flags against last word in args
        self.cleaned_args = AppArgumentsBuilder(None).map_short_flags(
            self.cleaned_args, vars(self.args_parser.get_parsed_args())
        )
        if not self.cleaned_args:
            print("App cleaned_args are not valid")
            local_valid = False

        self.valid = local_valid
        return self

    def run(self, name=None):
        if not self.valid:
            print("App is not valid.\nTrying to run anyway.")
            # print(self.context)
            if name is None:
                # Running without cleaned arguments that match context
                for name in self.context.context_holder.keys():
                    context = self.context.context_holder[name].command_queue.run_all()
                    self.output = context  # Add this line
                    print(
                        "DEBUG: Context name:", name
                    )  # Add this print statement for debugging
                    print("DEBUG: CommandQueue object:", context)  # Change this line
                    self.output = context_run.get_output()
                return self
            context_run = self.context.context_holder[name].command_queue.run_all()
            self.run_history.append(context_run.get_history())
            return self

        # print("App is valid")

        # Run all commands from cleaned arguments that match context
        if name is None:
            for name in self.cleaned_args.keys():
                if name in self.executables:
                    if name in self.context.context_holder.keys():
                        # print("Running command from args: ", name)
                        context_run = self.context.context_holder[
                            name
                        ].command_queue.run_all()
                        self.run_history.append(context_run.get_history())
                        # Add the following line to store the output after appending to run_history
                        self.output = context_run.get_output()
            return self

        # print("Running one command for context: ", name)
        context_run = self.context.context_holder[name].command_queue.run_all()
        self.run_history.append(context_run.get_history())
        return self

    def get_run_history(self):
        if len(self.run_history) == 0:
            print("No run history found")
            return []
        if len(self.run_history) == 1:
            return self.run_history[0]
        return self.run_history

    def clear_run_history(self):
        self.run_history = []
        return self

    def get_arg(self, name):
        try:
            # dotenv is in uppercase
            found_arg = self.config.get_setting(name.upper())
        except KeyError:
            SYSTEM_LOG.warning("No dotenv config set for: ", name)
            found_arg = None
        # flags have priority
        if name.lower() in self.cleaned_args.keys():
            found_arg = self.cleaned_args[name.lower()]
        return found_arg


class AppBuilder:
    def __init__(self, app=None):
        if app is None:
            self.app = App()
        else:
            self.app = app

    @property
    def context(self):
        return AppContextBuilder(self.app)

    @property
    def name(self):
        return AppNameBuilder(self.app)

    @property
    def args_parser(self):
        return AppArgsParserBuilder(self.app)

    @property
    def arguments(self):
        return AppArgumentsBuilder(self.app)

    @property
    def config(self):
        return MyAppConfigBuilder(self.app)

    def build(self):
        return self.app

    def validate(self):
        self.app.validate()
        return self

    def get_output(self):
        return self.output


class AppContextBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def add_context(self, context):
        if self.app.context is None:
            self.app.context = ContextHolder()
        self.app.context.add_context(context)
        return self

    def set_context(self, context):
        self.app.context = context
        return self


class AppNameBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def set_name(self, name):
        self.app.name = name
        return self


class AppArgsParserBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def add_argument(self, *args, **kwargs):
        if self.app.args_parser is None:
            self.app.args_parser = Parser().Factory.new(
                add_help=True, description="My app"
            )
        self.app.args_parser.add_argument(*args, **kwargs)
        return self

    def set_args_parser(self, args_parser):
        self.app.args_parser = args_parser
        return self


class AppArgumentsBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def set_arguments(self, arguments):
        self.app.arguments = arguments
        self.app.cleaned_args = self.clean_arg_function(arguments)
        return self

    def clean_arguments(self, arguments: list):
        self.app.cleaned_args = self.clean_arg_function(arguments)
        return self

    def set_executables(self, executables: list):
        self.app.executables = executables
        return self

    # TODO: This method needs work
    @staticmethod
    def map_short_flags(arguments, parsed_args):
        for arg in parsed_args.keys():
            clean = arg.split("_")[-1]
            if clean in arguments:
                # update dictionary with long flag
                arguments[arg] = arguments.pop(clean)
        return arguments

    @staticmethod
    def clean_arg_function(arguments: list) -> dict:
        cleaned_args = {}
        last_arg = None

        for arg in arguments:
            if arg.startswith("-") or arg.startswith("--"):
                cleaned_arg = arg.lstrip("-")
                if last_arg and cleaned_args[last_arg] == True:
                    cleaned_args[last_arg] = []
                last_arg = cleaned_arg
                if last_arg not in cleaned_args:
                    cleaned_args[last_arg] = True
            elif last_arg is not None:
                if cleaned_args[last_arg] == True:
                    cleaned_args[last_arg] = [arg]
                else:
                    cleaned_args[last_arg].append(arg)

        return cleaned_args

    @staticmethod
    def clean_arg_function_old(arguments: list):
        def is_flag(arg: str):
            return arg.startswith("--") or arg.startswith("-")

        def clean_arg(argument: str):
            if argument.startswith("--"):
                return argument.replace("--", "", 2).replace("-", "_")
            elif argument.startswith("-"):
                return argument.replace("-", "", 1).replace("-", "_")
            return argument

        arg_dict = {}
        args_list = []  # internal list
        argv_list = []  # internal list

        # clean args and return a dict
        for arg in arguments:
            if is_flag(arg):
                # Check remaining
                if len(args_list) == 1:
                    if len(argv_list) > 1:
                        arg_dict[clean_arg(args_list.pop())] = [
                            x for x in argv_list.pop()
                        ]
                    elif len(argv_list) == 1:
                        arg_dict[clean_arg(args_list.pop())] = argv_list.pop()
                    else:  # 0 or less
                        arg_dict[clean_arg(args_list.pop())] = None
                args_list.append(arg)
            else:
                argv_list.append(arg)

        if len(args_list) > 1:
            for x in args_list:
                arg_dict[clean_arg(x)] = None
            # Use the last one as the remainder for argv_list
            if len(argv_list) > 1:
                arg_dict[clean_arg(args_list.pop())] = [x for x in argv_list.pop()]
            elif len(argv_list) == 1:
                arg_dict[clean_arg(args_list.pop())] = argv_list.pop()
            else:  # 0 or less
                arg_dict[clean_arg(args_list.pop())] = None

        # normal case
        elif len(args_list) == 1:
            if len(argv_list) > 1:
                arg_dict[clean_arg(args_list.pop())] = [x for x in argv_list.pop()]
            elif len(argv_list) == 1:
                arg_dict[clean_arg(args_list.pop())] = argv_list.pop()
            else:  # 0 or less
                arg_dict[clean_arg(args_list.pop())] = None

        else:
            for x in argv_list:
                arg_dict[clean_arg(x)] = None

        return arg_dict


class MyAppConfigBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def set_config(self, config):
        self.app.config = config
        return self
