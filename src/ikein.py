#!/usr/bin/env python3

import importlib
import glob
from functools import reduce
import sys
import subprocess


def import_modules(folder_path):
    return reduce(lambda accumulate, current: {**accumulate, **current},
                  list(map(lambda init_file:
                           importlib.import_module(
                               f"{folder_path}.{init_file.split('/')[1]}").methods,
                           glob.glob(
                               f'{folder_path}/*/__init__.py')
                           )))


def main(methods, args, debug=False):
    try:
        output_command = methods[args[1]](*args[2:]).split()
        if debug:
            print(output_command)
        else:
            subprocess.run(output_command)
    except:
        print("Command not found")


if __name__ == "__main__":
    methods = import_modules("modules")
    main(methods, sys.argv, debug=True)
