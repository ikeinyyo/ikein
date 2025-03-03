import sys
from typing import Dict, List

from utils.core import LIST_METHOD
from utils.loads import load


def main(ikein_info: Dict, ikein_methods: Dict, methods: Dict, args: List[str]) -> None:
    """
    Main function that executes a command based on the provided arguments.

    Parameters:
        ikein_info (Dict): General information about the available methods.
        ikein_methods (Dict): Dictionary containing application-specific methods.
        methods (Dict): Dictionary containing other general available methods.
        args (List[str]): List of command-line arguments.
    """
    command: str = args[1] if len(args) > 1 else LIST_METHOD

    try:
        if command in ikein_methods:
            output_command = ikein_methods[command]["method"](ikein_info, *args[2:])
        else:
            output_command = methods[command]["method"](*args[2:])

        print("<<START_COMMAND>>")
        print(output_command)
        print("<<END_COMMAND>>")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    """
    Program entry point.
    Loads methods and information from the plugins module and executes main().
    """
    ikein_info, ikein_methods, methods = load("plugins")
    main(ikein_info, ikein_methods, methods, sys.argv)
