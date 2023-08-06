""""Main module for probable_fiesta app."""
import sys

from ..config.variables import PackageDef as pd
from ..config.variables import VariablesDef as vd
from ..app.builder.app_builder import AppBuilder
from ..config.default_config import get_config
from ..app.builder.context_factory import ContextFactory

def main(args=None):
    """Main function for probable_fiesta app.


    Args:
        args (list): List of arguments. Defaults to None.
    """
    # Get args from cli if not provided
    if not args:
        args = sys.argv[1:]

    default_config = get_config(log_name="probable_fiesta")

    # Get user cleaned args
    aB = AppBuilder()
    arg_dict = aB.arguments.clean_arg_function(args)  # cleaned args also at main_app.cleaned_args

    # Build main app
    aB = AppBuilder()
    main_app = aB\
        .name\
            .set_name("main_app")\
        .arguments\
            .set_arguments(args)\
        .args_parser\
            .add_argument("--test-app", type=str, help="test app builder")\
            .add_argument("--version", action='store_true', help="show version builder")\
            .add_argument("--repeat", type=str, help="repeat input")\
        .context\
            .add_context(ContextFactory.new_context_one_new_command(
                "test_app","test_app_func", lambda x: x, arg_dict['test_app'] if "test_app" in arg_dict else 'repeat'))\
            .add_context(ContextFactory.new_context_one_new_command(
                "version", "version", get_version, None))\
            .add_context(ContextFactory.new_context_one_new_command(
                "repeat", "repeat", repeat, arg_dict['repeat'] if 'repeat' in arg_dict else None))\
        .config\
            .set_config(default_config)\
        .validate()\
        .build()

    # Get parser error if any
    if main_app.args_parser.error:
        return main_app.args_parser.error

    # Run each command on main app against user args
    for command in main_app.cleaned_args.keys():
        main_app.run(command)

    # Get command execution history
    history = main_app.get_run_history()
    print(history)
    return history

# Get current name and version from config
def get_version() -> str:
    """Get package version.

    Returns:
        str: Current package version.
    """
    return f"{pd.NAME} v.{vd.VERSION}"

def repeat(x):
    return(f"Repeating: {x}")

if __name__ == "__main__":
    main(sys.argv[1:])