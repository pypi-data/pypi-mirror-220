class Config():
    def __init__(self, package={}, logger=None, variables={}, dotenv=None):
        # properties
        self.package = package
        self.logger = logger
        self.variables = variables
        self.dotenv = dotenv
        # parsed dotenv properties
        self.parsed_dotenv = {}

    def __str__(self):
        return f"Config: {self.__dict__}"

    def get_setting(self, name):
        try:
            return self.parsed_dotenv[name]
        except KeyError:
            #print("No dotenv config set for: ", name)
            return None