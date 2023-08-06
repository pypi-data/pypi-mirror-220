from abc import ABC
from enum import Enum, auto
from .app_builder import AppBuilder
from ...config.builder.config_builder_factory import ConfigFactory

class App(ABC):
    def run(self):
        pass

class MyApp(App):
    def run(self):
        print("This is the my app")

class FlaskApp(App):
    def run(self):
        print("This is the flask app")

class AppFactory(ABC):
    def create_app(self, name, context, args_parse, args, config):
        pass

    def prepare_default(self):
        pass

class FlaskFactory(AppFactory):
    def create_app(self, name, context, args_parse, args, config):
        print("Creating flask app")
        my_app_builder = AppBuilder()
        config = ConfigFactory.new_config_builder('flask' , 'flask_factory').build()
        #logger = get_config('flask', 'flask_factory')
        my_app = my_app_builder\
            .name\
                .set_name(name)\
            .context\
                .set_context(context)\
            .args_parse\
                .set_args_parse(args_parse)\
            .arguments\
                .set_arguments(args)\
            .config\
                .set_config(config)\
            .build()
        return my_app


class AppMachine:
    class AvailableApps(Enum):
        APP = auto()
        FLASK = auto()
    
    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
            for d in self.AvailableApps:
                name = d.name[0] +  d.name[1:].lower()
                factory_name = name + "Factory"
                factory_instance = eval(factory_name)()
                self.factories.append((name, factory_instance))

    def __str__(self):
        return f"AppMachine: Available apps: {self.factories}"

    def prepare_app(self):
        print("Available apps:")
        for f in self.factories:
            print(f[0])
        s = input(f'Please pick app (0-{len(self.factories)-1}):')
        idx = int(s)
        # specify app name
        return self.factories[idx][1].prepare()

    def prepare_default_app(self):
        return self.factories[0][1].prepare_default()

def create_app(type):
    if type == 'app':
        return AppFactory().create_app()
    elif type == 'metrics_app':
        return FlaskFactory().create_app()
    else:
        print("Invalid app type")
        return None

def prepare_default_app(type):
    if type == 'app':
        return AppFactory().prepare_default()
    else:
        print("Only my_app is supported")
        return None
