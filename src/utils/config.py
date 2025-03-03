import json
import os
from typing import Dict


def get_config() -> None:
    file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    filepath = os.path.join(file_directory, "config.json")
    with open(filepath, "r") as in_file:
        return json.load(in_file)


def save_config(configuration: Dict) -> None:
    file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    filepath = os.path.join(file_directory, "config.json")
    with open(filepath, "w") as out_file:
        return json.dump(configuration, out_file, indent=4)
