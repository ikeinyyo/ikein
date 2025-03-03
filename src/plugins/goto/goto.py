import os

from utils.bash import echo, precho
from utils.config import get_config, save_config


def goto(*args):
    """Dispatches the goto command to the appropriate method based on the provided argument."""
    if not args:
        return echo("Invalid usage. Use: ikein usage goto for more information.")

    method = methods.get(args[0], _navigate)
    return method(*args)


def _load_goto_aliases():
    """Loads saved directory aliases from the configuration."""
    return get_config().get("goto", {}).get("dirs", {})


def _save_goto_aliases(dirs):
    """Saves the updated directory aliases to the configuration."""
    config = get_config()
    config.setdefault("goto", {})["dirs"] = dirs
    dirs.pop("key", None)  # Ensures 'key' is not mistakenly stored
    save_config(config)


def _add_alias(*args):
    """Adds a new directory alias."""
    if len(args) != 2:
        return echo("Invalid format. Use: goto -a <alias>")

    dirs = _load_goto_aliases()
    alias, directory = args[1], os.getcwd()
    dirs[alias] = directory
    _save_goto_aliases(dirs)

    return echo(f"Alias added: {alias} → {directory}")


def _remove_alias(*args):
    """Removes an existing directory alias."""
    if len(args) != 2:
        return echo("Invalid format. Use: goto -r <alias>")

    dirs = _load_goto_aliases()
    alias = args[1]

    if alias in dirs:
        del dirs[alias]
        _save_goto_aliases(dirs)
        return echo(f"Alias removed: {alias}")

    return echo(f"Alias not found: '{alias}'")


def _list_aliases(_):
    """Lists all saved directory aliases."""
    dirs = _load_goto_aliases()
    if not dirs:
        return echo("No saved aliases.")

    alias_list = "\n".join(f"\t- {key} → {path}" for key, path in dirs.items())
    return echo(f"Saved aliases:\n{alias_list}")


def _open_directory(*args):
    """Opens the directory associated with the given alias in the system's file manager."""
    if len(args) != 2:
        return echo("Invalid format. Use: goto -o <alias>")

    dirs = _load_goto_aliases()
    alias = args[1]

    if alias in dirs:
        precho(f"Opening directory: {dirs[alias]}")
        return f"open {dirs[alias]}"

    return echo(f"Alias not found: '{alias}'")


def _navigate(*args):
    """Navigates to a directory associated with a given alias."""
    if len(args) != 1:
        return echo("Invalid format. Use: goto <alias>")

    dirs = _load_goto_aliases()
    alias = args[0]

    if alias in dirs:
        precho(f"Navigating to: {dirs[alias]}")
        return f"cd {dirs[alias]}"

    return echo(f"Alias not found: '{alias}'")


methods = {
    "-a": _add_alias,
    "-l": _list_aliases,
    "-r": _remove_alias,
    "-o": _open_directory,
}
