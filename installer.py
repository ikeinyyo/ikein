import argparse
import json
import os
import shutil
import subprocess

SRC_DIRECTORY = "src"
CONSOLE_FILE = ".zshrc"

FILES_TO_COPY = ["ikein.py", "ikein.sh"]
DIRECTORIES_TO_COPY = ["plugins", "utils"]
ALIAS_NAME = "ikein"
CONFIGURATION_FILE = "config.json"


def initialize(root_path, purge):
    create_root_directory(root_path, purge)
    copy(root_path, FILES_TO_COPY, is_directory=False)
    copy(root_path, DIRECTORIES_TO_COPY, is_directory=True)


def create_root_directory(root_path, purge):
    if os.path.exists(root_path) and purge:
        shutil.rmtree(root_path)
        print(f"Deleting '{root_path}' directory...")
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    print(f"Creating '{root_path}' directory...")


def copy(root_path, item_paths, is_directory=False):
    for item_path in item_paths:
        print(f"Copying '{item_path}' to {root_path}...")
        if is_directory:
            shutil.copytree(
                os.path.join(SRC_DIRECTORY, item_path),
                os.path.join(root_path, item_path),
                dirs_exist_ok=True,
            )
        else:
            shutil.copy(
                os.path.join(SRC_DIRECTORY, item_path),
                os.path.join(root_path, item_path),
            )


def add_execution_permision(script_path):
    print(f"Adding execution permission to '{script_path}'...")
    subprocess.run(f"chmod +x {script_path}", shell=True)


def add_alias(script_path):
    alias_command = f"source {script_path}"
    print(f"Removing previous alias '{ALIAS_NAME}'...")
    clear_alias(ALIAS_NAME)
    print(f"Adding alias {ALIAS_NAME} for '{alias_command}'...")
    subprocess.run(
        f"echo \"alias {ALIAS_NAME}='{alias_command}'\" >> ~/{CONSOLE_FILE}", shell=True
    )


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
            f"The alias '{alias_name}' already existed and was removed from the {CONSOLE_FILE} file."
        )
    else:
        print(f"The alias '{alias_name}' does not exist in the {CONSOLE_FILE} file.")


def update_configuration_file(root_path):
    ikein_config_file = os.path.join(root_path, CONFIGURATION_FILE)
    local_config_file = os.path.join("src", CONFIGURATION_FILE)

    if not os.path.exists(ikein_config_file):
        print("Creating configuration file...")
        os.makedirs(os.path.dirname(ikein_config_file), exist_ok=True)
        with open(local_config_file, "r") as src:
            with open(ikein_config_file, "w") as dest:
                dest.write(src.read())
        return

    with open(local_config_file, "r") as src:
        local_config = json.load(src)

    with open(ikein_config_file, "r") as dest:
        ikein_config = json.load(dest)

    merged_config = {
        **local_config,
        **ikein_config,
    }

    with open(ikein_config_file, "w") as dest:
        print("Updating configuration file...")
        json.dump(merged_config, dest, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--purge", action="store_true", help="Activa el modo purge", required=False
    )
    args = parser.parse_args()

    entry_point = "ikein.sh"
    root_path = os.path.expanduser("~/ikein")
    script_path = os.path.join(root_path, entry_point)
    initialize(root_path, args.purge)
    add_execution_permision(script_path)
    add_alias(script_path)
    update_configuration_file(root_path)
