# probable-fiesta

[![Python application](https://github.com/sergio-munoz/probable-fiesta/actions/workflows/python_app.yml/badge.svg)](https://github.com/sergio-munoz/probable-fiesta/actions/workflows/python_app.yml) [![Upload Python Package Production](https://github.com/sergio-munoz/probable-fiesta/actions/workflows/python_publish.yml/badge.svg)](https://github.com/sergio-munoz/probable-fiesta/actions/workflows/python_publish.yml) [![wakatime](https://wakatime.com/badge/user/1e0e8b49-a94f-431f-8ca2-93081dfb4c8b/project/0dca8cc1-046e-4345-a174-50d11cad482b.svg)](https://wakatime.com/badge/user/1e0e8b49-a94f-431f-8ca2-93081dfb4c8b/project/0dca8cc1-046e-4345-a174-50d11cad482b)

> There's probably a fiesta somewhere.

Python Package Core 

A Python package core for building a Python package.

## Installation

## Installation using pip


```bash
pip install probable-fiesta
```

## Installation with automatic build and install


> It is recommended to setup a [virtual environment](https://docs.python.org/3/library/venv.html).

To install locally with automatic build and install, run the following command in the root directory of the project.

```bash
git clone https://github.com/sergio-munoz/probable-fiesta.git
cd probable-fiesta
chmod +x scripts/build_install.sh
./scripts/build_install.sh
```

## Installation with manual build and install

Setup a new virtual environment and install packages in `requirements.txt`.

```bash
python -m venv build_venv
source build_venv/bin/activate
(build_venv) $ pip install -r build_requirements.txt
(build_venv) $ hatch build
(build_venv) $ pip install dist/probable_fiesta-${VERSION}.tar.gz
```

### Installation in Jupyter Notebook

To install the into the Jupyter Notebook kernel:

```bash
import sys
!{sys.executable} -m pip install -U --no-deps probable-fiesta
```

## Usage

```bash
probable_fiesta --help
```

## Build and Run

### Build and Run command

Build and a command. Pass flags, for example `--version`:

```bash
./scripts/build_install.sh & probable_fiesta --version
```

## Tests

### Automatic

```bash
./scripts/test_coverage.sh
```

## Developer Reference

This package contains various modules that can be used to build a Python package.

### Modules

- `probable_fiesta`: Main module.
- `probable_fiesta.app`: Main application.
- `probable_fiesta.app.main`: Main application.
- `probable_fiesta.cli`: Command line interface.
- `probable_fiesta.command`: Internal command implementation.
- `probable_fiesta.config`: Configuration.
- `probable_fiesta.logger`: Logging.

### Create Application Example

Create a new application using the `probable_fiesta` package.

- Create a main module, for example `main.py`:

```python
# Path: main.py
from probable_fiesta.config.variables import DotEnvDef
from probable_fiesta.config.builder.config_builder import ConfigBuilder
from probable_fiesta.logger.builder.logger_factory import LoggerFactory
from probable_fiesta.app.builder.context_factory import ContextFactory as CF
from probable_fiesta.app.builder.app_builder import AppBuilder

# Import or add your business logic here
# For example the next get version functions:
def get_version_echo(version):
    return version
def get_version():
    return "v0"

# Create custom dotenv definition from DotEnvDef
class MyDotEnvDef(DotEnvDef):
    def __init__(self):
        super().__init__()
        self.version_echo = "v0" # This will be overwritten by .env file

    # make the class iterable
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield value  # only yield the values

# Create main function
def main(args):
    # Create config, will be replaced by a Factory in the future
    cB = ConfigBuilder()
    config = (
        cB.logger.set_logger(
            LoggerFactory.new_logger_get_logger("main_app", "INFO")
        )
        .dotenv.load_dotenv()  # Load .env file if exists
        .set_vars(MyDotEnvDef())
        .build()
    )

    # Create main app
    main_app = (
        aB.name.set_name("main_app")
        .arguments.set_arguments(args)
        # Add your arguments
        .args_parser.add_argument(
            "--version", action="store_true", help="show version builder"
        )
        # Add your commands that do not require parsed arguments
        .context.add_context(
            CF.new_context_one_new_command("version", "version", get_version, None)
        )
        # Define which are executable
        .set_executables(["version"])
        .config.set_config(config)
        .validate()
        .build()
    )

    # Create commands that require parsed arguments
    c3 = CF.new_context_one_new_command(
        "--version-echo",
        "version_echo",
        get_version_echo,
        main_app.get_arg("version_echo"),  # CLI overrides .env
    )
    # Add commands to main app
    main_app.context.add_context(c3)

    # Check build errors
    if main_app.args_parser.error:
        print(main_app.args_parser.error)
        return

    # Run main app
    run_context = main_app.run()
    history = run_context.get_run_history()
    print(history)
    return history
```

This allows you to call the `main` function from the command line:

```bash
python main.py --version
```
