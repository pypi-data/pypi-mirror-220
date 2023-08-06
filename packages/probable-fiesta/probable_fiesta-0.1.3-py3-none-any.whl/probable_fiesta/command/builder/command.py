class Command:
    def __init__(self, name, function, *args):
        self.name = name
        self.function = function
        self.args = args

    def __str__(self):
        return f"Command: {self.__dict__}"

    def invoke(self, input=None):
        if self.function is not None and self.args is not None:
            if input is not None:
                return self.function(input, *self.args)
            else:
                return self.function(*self.args)
        return None

    class Factory:
        @staticmethod
        def new_command(name, function, *args):
            return Command(name, function, *args)

    factory = Factory()
