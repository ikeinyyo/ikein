from typing import List

from utils.bash import echo
from utils.config import get_config


def repeat(*args: List[str]) -> str:
    """
    Repeats the provided message.

    If a message is provided as an argument, it will repeat the provided message.

    Parameters:
        args (List[str]): The list of arguments, where the first argument (if provided) is used as the name.

    Returns:
        str: The original message.
    """
    if len(args):
        return echo(args[0])
    else:
        return echo("Invalid usage. Use: ikein echo <message>")


def say_hello(*args: List[str]) -> str:
    """
    Greets the user with a personalized message.

    If a name is provided as an argument, it will greet the provided name.
    Otherwise, it will greet the name stored in the configuration under 'displayName'.

    Parameters:
        args (List[str]): The list of arguments, where the first argument (if provided) is used as the name.

    Returns:
        str: A greeting message.
    """
    if len(args):
        return echo(f"Hi {args[0]}")
    return echo(f"Hi {get_config().get('displayName', '')}!")
