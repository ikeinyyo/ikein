import sys
from typing import Dict, List

from utils.bash import echo
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
    plugin: str = args[1] if len(args) > 1 else LIST_METHOD
    command: str = args[2] if len(args) > 2 else ""

    try:
        if plugin in ikein_info:
            args = args[3:] if command in ikein_info[plugin] else args[2:]
            command = command if command in ikein_info[plugin] else plugin
            output_command = ikein_info[plugin][command]["method"](*args)
        elif plugin in ikein_info["ikein"]:
            output_command = ikein_info["ikein"][plugin]["method"](
                ikein_info, *args[2:]
            )
        else:
            output_command = echo("Command not found")

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
