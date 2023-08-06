from .my_args_parser import MyArgsParser


class Parser:
    def __init__(self, parser=None, add_help=True, description=None):
        if parser is not None:
            self.parser = parser
        else:
            self.parser = MyArgsParser(add_help=add_help, description=description)
        self.valid = False
        self.parsed_args = None  # validated arguments
        self.error = None

    def __str__(self):
        return f"Parser: {self.__dict__}"

    def add_argument(self, *args, **kwargs):
        if not args:
            print("No args to parse")
            return None
        if not kwargs:
            self.parser.add_argument(*args)
        else:
            self.parser.add_argument(*args, **kwargs)
        return self

    def parse_args(self, args):
        self.parsed_args = self.parser.parse_args(args)
        return self.parsed_args

    def get_parsed_args(self):
        return self.parsed_args

    def get_parsed_arg(self, arg):
        if not self.parsed_args:
            print("parse args first.")
            return None
        if arg in self.parsed_args:
            a = self.parsed_args.__dict__.get(arg)
            return a
        return None

    def validate(self, args=None):
        self.valid = True
        self.parsed_args = self.parser.parse_args(args)
        if self.parser.error_message:
            self.error = self.parser.error_message
            self.valid = False
        if not self.parsed_args:
            self.valid = False
        return self

    @staticmethod
    def new(parser=None, add_help=True, description=None):
        return Parser(parser, add_help, description)

    class Factory:
        @staticmethod
        def new(parser=None, add_help=True, description=None):
            return Parser.new(parser, add_help, description)

    factory = Factory()
