import json
import os


def get_config():
    file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    filepath = os.path.join(file_directory, "config.json")
    with open(filepath, "r") as in_file:
        return json.load(in_file)
