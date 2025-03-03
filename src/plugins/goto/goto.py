import os
from typing import Callable, Dict, List

from utils.bash import echo, precho
from utils.config import get_config, save_config


def goto(*args: str) -> str:
    """
    Dispatches the goto command to the appropriate method based on the provided argument.

    Parameters:
        args (str): Command arguments for the goto operation.

    Returns:
        str: The result of the command operation (e.g., a message or action).
    """
    if not args:
        return echo("Invalid usage. Use: ikein usage goto for more information.")

    method: Callable[..., str] = methods.get(args[0], _navigate)
    return method(*args)


def _load_goto_aliases() -> Dict[str, str]:
    """
    Loads saved directory aliases from the configuration.

    Returns:
        dict: A dictionary of directory aliases where the key is the alias and the value is the directory path.
    """
    return get_config().get("goto", {}).get("dirs", {})


def _save_goto_aliases(dirs: Dict[str, str]) -> None:
    """
    Saves the updated directory aliases to the configuration.

    Parameters:
        dirs (dict): A dictionary of directory aliases to save.
    """
    config = get_config()
    config.setdefault("goto", {})["dirs"] = dirs
    dirs.pop("key", None)  # Ensures 'key' is not mistakenly stored
    save_config(config)


def _add_alias(*args: str) -> str:
    """
    Adds a new directory alias.

    Parameters:
        args (str): The alias and directory for the new alias.

    Returns:
        str: Confirmation message about the alias addition.
    """
    if len(args) != 2:
        return echo("Invalid format. Use: goto -a <alias>")

    dirs = _load_goto_aliases()
    alias, directory = args[1], os.getcwd()
    dirs[alias] = directory
    _save_goto_aliases(dirs)

    return echo(f"Alias added: {alias} → {directory}")


def _remove_alias(*args: str) -> str:
    """
    Removes an existing directory alias.

    Parameters:
        args (str): The alias to remove.

    Returns:
        str: Confirmation message about the alias removal or error message.
    """
    if len(args) != 2:
        return echo("Invalid format. Use: goto -r <alias>")

    dirs = _load_goto_aliases()
    alias = args[1]

    if alias in dirs:
        del dirs[alias]
        _save_goto_aliases(dirs)
        return echo(f"Alias removed: {alias}")

    return echo(f"Alias not found: '{alias}'")


def _list_aliases(_) -> str:
    """
    Lists all saved directory aliases.

    Parameters:
        _: Unused argument to match function signature.

    Returns:
        str: A list of all saved aliases, or a message indicating no aliases are saved.
    """
    dirs = _load_goto_aliases()
    if not dirs:
        return echo("No saved aliases.")

    alias_list = "\n".join(f"\t- {key} → {path}" for key, path in dirs.items())
    return echo(f"Saved aliases:\n{alias_list}")


def _open_directory(*args: str) -> str:
    """
    Opens the directory associated with the given alias in the system's file manager.

    Parameters:
        args (str): The alias to open.

    Returns:
        str: A command to open the directory, or an error message if the alias is not found.
    """
    if len(args) != 2:
        return echo("Invalid format. Use: goto -o <alias>")

    dirs = _load_goto_aliases()
    alias = args[1]

    if alias in dirs:
        precho(f"Opening directory: {dirs[alias]}")
        return f"open {dirs[alias]}"

    return echo(f"Alias not found: '{alias}'")


def _navigate(*args: str) -> str:
    """
    Navigates to a directory associated with a given alias.

    Parameters:
        args (str): The alias to navigate to.

    Returns:
        str: A command to navigate to the directory, or an error message if the alias is not found.
    """
    if len(args) != 1:
        return echo("Invalid format. Use: goto <alias>")

    dirs = _load_goto_aliases()
    alias = args[0]

    if alias in dirs:
        precho(f"Navigating to: {dirs[alias]}")
        return f"cd {dirs[alias]}"

    return echo(f"Alias not found: '{alias}'")


methods: Dict[str, Callable[..., str]] = {
    "-a": _add_alias,
    "-l": _list_aliases,
    "-r": _remove_alias,
    "-o": _open_directory,
}
