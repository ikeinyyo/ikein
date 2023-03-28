#!/usr/bin/env python3
import os
import shutil
import subprocess

SRC_DIRECTORY = "src"
CONSOLE_FILE = ".zshrc"


def main():
    entry_point = "ikein.py"
    root_path = os.path.expanduser('~/ikein')
    script_path = os.path.join(root_path, entry_point)
    initialize(root_path)
    add_execution_permision(script_path)
    add_alias(script_path)


def initialize(root_path):
    files_to_copy = ['ikein.py']
    directories_to_copy = ['modules']

    create_root_directory(root_path)
    copy(root_path, files_to_copy, is_directory=False)
    copy(root_path, directories_to_copy, is_directory=True)


def create_root_directory(root_path):
    if os.path.exists(root_path):
        shutil.rmtree(root_path)
        print(f"Deleting '{root_path}' directory...")
    os.makedirs(root_path)
    print(f"Creating '{root_path}' directory...")


def copy(root_path, item_paths, is_directory=False):
    for item_path in item_paths:
        print(f"Copying '{item_path}' to {root_path}...")
        if is_directory:
            shutil.copytree(os.path.join(SRC_DIRECTORY, item_path),
                            os.path.join(root_path, item_path), dirs_exist_ok=True)
        else:
            shutil.copy(os.path.join(SRC_DIRECTORY, item_path),
                        os.path.join(root_path, item_path))


def add_execution_permision(script_path):
    print(f"Adding execution permission to '{script_path}'...")
    subprocess.run(
        f'chmod +x {script_path}', shell=True)


def add_alias(script_path):
    alias_name = "ikein"
    alias_command = f"python {script_path}"
    print(f"Removing previous alias '{alias_name}'...")
    clear_alias(alias_name)
    print(
        f"Adding alias {alias_name} for '{alias_command}'...")
    subprocess.run(
        f'echo "alias {alias_name}=\'{alias_command}\'" >> ~/{CONSOLE_FILE}', shell=True)


def clear_alias(alias_name):
    bashrc_file = os.path.expanduser(f"~/{CONSOLE_FILE}")

    with open(bashrc_file, "r") as f:
        lines = f.readlines()

    alias_exists = False
    for line in lines:
        if f"alias {alias_name}=" in line:
            alias_exists = True
            break

    if alias_exists:
        os.system(f"cp {bashrc_file} {bashrc_file}.bak")
        with open(bashrc_file, "w") as f:
            for line in lines:
                if f"alias {alias_name}=" not in line:
                    f.write(line)
        print(
            f"The alias '{alias_name}' already existed and was removed from the {CONSOLE_FILE} file.")
    else:
        print(
            f"The alias '{alias_name}' does not exist in the {CONSOLE_FILE} file.")


if __name__ == "__main__":
    main()
