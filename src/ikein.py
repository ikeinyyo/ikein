#!/usr/bin/env python3

import glob
import importlib
import os
import subprocess
import sys
from functools import reduce


def import_modules(folder_path):
    current_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    methods = reduce(lambda accumulate, current: {**accumulate, **current},
                     list(map(lambda init_file:
                              importlib.import_module(
                                  f"{folder_path}.{init_file.split('/')[-2]}").methods,
                              glob.glob(
                                  f'{folder_path}/*/__init__.py')
                              )))

    os.chdir(current_dir)

    return methods


def list_methods(methods):
    for method in methods.keys():
        print(method)
    return ""


def load_ikein_methods():
    return {
        'list': list_methods
    }


def main(ikein_methods, methods, args, debug=False):
    command = args[1]
    try:
        if command in ikein_methods:
            output_command = ikein_methods[command](methods).split()
        else:
            output_command = methods[command](*args[2:]).split()

        if debug:
            print(output_command)
        elif output_command:
            subprocess.run(output_command)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    methods = import_modules("modules")
    ikein_methods = load_ikein_methods()
    main(ikein_methods, methods, sys.argv, debug=False)
