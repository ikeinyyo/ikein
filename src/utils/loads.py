import glob
import importlib
import os
from functools import reduce
from typing import Dict


def import_plugins(folder_path: str) -> Dict:
    """
    Imports plugins from the specified folder and returns a dictionary of methods.

    Parameters:
        folder_path (str): Path to the plugins directory.

    Returns:
        Dict: A dictionary mapping plugin names to their respective methods.
    """
    current_dir = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    methods = reduce(
        lambda accumulate, current: {**accumulate, **current},
        list(
            map(
                lambda init_file: {
                    init_file.split("/")[-2]: importlib.import_module(
                        f"{folder_path}.{init_file.split('/')[-2]}"
                    ).methods
                },
                glob.glob(f"{folder_path}/*/__init__.py"),
            )
        ),
    )
    os.chdir(current_dir)
    return methods


def flatten_methods(nested_dict: Dict) -> Dict:
    """
    Flattens a nested dictionary of methods into a single-level dictionary.

    Parameters:
        nested_dict (Dict): A dictionary containing nested method dictionaries.

    Returns:
        Dict: A flattened dictionary with all methods at the top level.
    """
    flat_dict = {}
    for methods in nested_dict.values():
        flat_dict.update(methods)
    return flat_dict


def load(plugins_path: str) -> tuple[Dict, Dict, Dict]:
    """
    Loads plugins and their methods, returning structured dictionaries.

    Parameters:
        plugins_path (str): Path to the plugins directory.

    Returns:
        tuple[Dict, Dict, Dict]:
            - ikein_info: Dictionary containing all methods from core and plugins.
            - ikein_methods: Flattened dictionary of core methods.
            - methods: Flattened dictionary of all loaded methods.
    """
    from .core import methods as ikein_methods

    methods = import_plugins(plugins_path)
    ikein_info = ikein_methods.copy()
    ikein_info.update(methods)
    methods = flatten_methods(methods)
    ikein_methods = flatten_methods(ikein_methods)
    return ikein_info, ikein_methods, methods
