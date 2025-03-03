import os

from .bash import printsh


def list_methods(ikein_info):
    for category in ikein_info:
        printsh(f"- {category}")
        for method in ikein_info[category]:
            printsh(f"\t- {method}: {ikein_info[category][method]['info']}")
    return ""


def usage_method(ikein_info, *args):
    for category in ikein_info:
        for method in ikein_info[category]:
            if method == args[0]:
                printsh(f"- {ikein_info[category][method]['info']}:")
                printsh(f"\t$ {ikein_info[category][method]['usage']}")
    return ""


def open_configuration(_):
    file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    return f"code {os.path.join(file_directory, 'config.json')}"


methods = {
    "ikein": {
        "list": {
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
