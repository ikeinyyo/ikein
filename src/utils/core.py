import os
from typing import Any, Dict

from .bash import printsh

LIST_METHOD = "list"


def list_methods(ikein_info: Dict[str, Dict[str, Any]]) -> str:
    """
    Displays all available IKEIN commands grouped by category.

    Parameters:
        ikein_info (Dict[str, Dict[str, Any]]): Dictionary containing command categories and their methods.

    Returns:
        str: An empty string as output control.
    """
    for category in ikein_info:
        printsh(f"- {category}")
        for method in ikein_info[category]:
            printsh(f"\t- {method}: {ikein_info[category][method]['info']}")
    return ""


def usage_method(ikein_info: Dict[str, Dict[str, Any]], *args: str) -> str:
    """
    Provides usage details for a specific command.

    Parameters:
        ikein_info (Dict[str, Dict[str, Any]]): Dictionary containing command categories and their methods.
        args (str): Command name to retrieve usage information.

    Returns:
        str: An empty string as output control.
    """
    for category in ikein_info:
        for method in ikein_info[category]:
            if method == args[0]:
                printsh(f"- {ikein_info[category][method]['info']}:")
                printsh(f"\t$ {ikein_info[category][method]['usage']}")
    return ""


def open_configuration(_: Any) -> str:
    """
    Returns the command to open the IKEIN configuration JSON file.

    Parameters:
        _ (Any): Placeholder parameter (not used).

    Returns:
        str: Command to open the configuration file.
    """
    file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    return f"code {os.path.join(file_directory, 'config.json')}"


methods: Dict[str, Dict[str, Dict[str, Any]]] = {
    "ikein": {
        LIST_METHOD: {
            "method": list_methods,
            "info": "Displays all available IKEIN commands.",
            "usage": "ikein list",
        },
        "usage": {
            "method": usage_method,
            "info": "Provides usage details for a specific command.",
            "usage": "ikein usage [command]",
        },
        "config": {
            "method": open_configuration,
            "info": "Open the IKEIN configuration JSON file for editing.",
            "usage": "ikein config",
        },
    }
}
