import os
import subprocess
from typing import Callable, Dict, List

from utils.bash import echo, precho
from utils.config import get_config, save_config


def run(*args: str) -> str:
    """
    Dispatches the run command to the appropriate method based on the provided argument.

    Parameters:
        args (str): Command arguments for the run operation.

    Returns:
        str: The result of the command operation (e.g., a message or action).
    """
    if not args:
        return echo("Invalid usage. Use: ikein usage run for more information.")

    method: Callable[..., str] = methods.get(args[0], _execute_command)
    return method(*args)


def _load_run_aliases() -> Dict[str, Dict[str, str]]:
    """
    Loads saved run aliases from the configuration.

    Returns:
        dict: A dictionary of run aliases where the key is the alias and the value is a dictionary containing the directory and command.
    """
    return get_config().get("run", {}).get("commands", {})


def _save_run_aliases(commands: Dict[str, Dict[str, str]]) -> None:
    """
    Saves the updated run aliases to the configuration.

    Parameters:
        commands (dict): A dictionary of run aliases to save.
    """
    config = get_config()
    config.setdefault("run", {})["commands"] = commands
    commands.pop("key", None)  # Ensures 'key' is not mistakenly stored
    save_config(config)


def _add_alias(*args: str) -> str:
    """
    Adds a new run alias.

    Parameters:
        args (str): The alias and command for the new alias.

    Returns:
        str: Confirmation message about the alias addition.
    """
    if len(args) < 2:
        return echo("Invalid format. Use: run -a <alias> <command>")

    commands = _load_run_aliases()
    alias, directory, command = args[1], os.getcwd(), " ".join(args[2:])
    commands[alias] = {"directory": directory, "command": command}
    _save_run_aliases(commands)

    return echo(f"Alias added: {alias} → {directory} {command}")


def _remove_alias(*args: str) -> str:
    """
    Removes an existing run alias.

    Parameters:
        args (str): The alias to remove.

    Returns:
        str: Confirmation message about the alias removal or error message.
    """
    if len(args) != 2:
        return echo("Invalid format. Use: run -r <alias>")

    commands = _load_run_aliases()
    alias = args[1]

    if alias in commands:
        del commands[alias]
        _save_run_aliases(commands)
        return echo(f"Alias removed: {alias}")

    return echo(f"Alias not found: '{alias}'")


def _list_aliases(_) -> str:
    """
    Lists all saved run aliases.

    Parameters:
        _: Unused argument to match function signature.

    Returns:
        str: A list of all saved aliases, or a message indicating no aliases are saved.
    """
    commands = _load_run_aliases()
    if not commands:
        return echo("No saved aliases.")

    alias_list = "\n".join(
        f"\t- {key} → {commands[key]['directory']} {commands[key]['command']}"
        for key in commands
    )
    return echo(f"Saved aliases:\n{alias_list}")


def _execute_command(*args: str) -> str:
    """
    Executes a command associated with a given alias.

    Parameters:
        args (str): The alias to execute.

    Returns:
        str: A command to navigate to the directory and execute the associated command, or an error message if the alias is not found.
    """
    if len(args) != 1:
        return echo("Invalid format. Use: run <alias>")

    commands = _load_run_aliases()
    alias = args[0]

    if alias in commands:
        return f"cd {commands[alias]['directory']}; {commands[alias]['command']}; cd {os.getcwd()};"

    return echo(f"Alias not found: '{alias}'")


methods: Dict[str, Callable[..., str]] = {
    "-a": _add_alias,
    "-l": _list_aliases,
    "-r": _remove_alias,
}
