from .parser_builder import ParserBuilder

class ParserFactory:
    """Factory for creating an args parser."""
    def __init__(self):
        pass

    def new(self, *args, **kwargs):
        pB = ParserBuilder()

        parser = pB.parser.create_new_args_parser()

        parser.add_argument(*args, **kwargs)

        parser.build()

        return parser.get_args_parser()

    def new_only_args(self, *args):
        pB = ParserBuilder()
        parser = pB.parser.create_new_args_parser()
        parser.add_argument(*args)
        parser.build()

        return parser.get_args_parser()