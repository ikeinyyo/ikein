import json
import os
from typing import Any, Dict


def get_config() -> Dict[str, Any]:
    """
    Loads and returns the configuration from the config.json file.

    Returns:
        Dict[str, Any]: The configuration data as a dictionary.
    """
    file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    filepath = os.path.join(file_directory, "config.json")
    with open(filepath, "r") as in_file:
        return json.load(in_file)


def save_config(configuration: Dict[str, Any]) -> None:
    """
    Saves the given configuration to the config.json file.

    Parameters:
        configuration (Dict[str, Any]): The configuration data to be saved.
    """
    file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    filepath = os.path.join(file_directory, "config.json")
    with open(filepath, "w") as out_file:
        json.dump(configuration, out_file, indent=4)
