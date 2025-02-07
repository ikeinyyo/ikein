import glob
import importlib
import os
from functools import reduce


def import_plugins(folder_path):

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


def flatten_methods(nested_dict):
    flat_dict = {}
    for methods in nested_dict.values():
        flat_dict.update(methods)
    return flat_dict


def load(plugins_path: str):
    from .core import methods as ikein_methods

    methods = import_plugins(plugins_path)
    ikein_info = ikein_methods.copy()
    ikein_info.update(methods)
    methods = flatten_methods(methods)
    ikein_methods = flatten_methods(ikein_methods)
    return ikein_info, ikein_methods, methods
