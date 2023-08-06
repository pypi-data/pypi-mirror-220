from .parser import Parser

class ParserBuilder:

    def __init__(self, args_parser=None):
        if args_parser is not None:
            self.args_parser = args_parser
        else:
            self.args_parser = Parser.Factory.new()

    @property
    def parser(self):
        return ParserBuilderParser(self.args_parser)
    
    def validate(self, args):
        return self.args_parser.validate(args)

    def build(self):
        return self

class ParserBuilderParser(ParserBuilder):

    def __init__(self, args_parser):
        super().__init__(args_parser)

    def set_args_parser(self, args_parser):
        self.args_parser = args_parser
        return self

    def add_argument(self, *args, **kwargs):
        self.args_parser.add_argument(*args, **kwargs)
        return self

    def parse_args(self, args=None):
        if not self.args_parser.parser:
            print("No parser found.")
            return None
        self.args_parser.parse_args(args)
        return self

    def get_parsed_args(self):
        return self.args_parser.parser.get_parsed_args()