import re
import sys
from typing import Dict

IKEIN_NAME = "- [I.K.E.I.N.]"


def __escape_special_characters(text: str) -> str:
    """
    Escapes special characters in a given text to ensure proper formatting.

    Parameters:
        text (str): The input text to escape.

    Returns:
        str: The escaped text with special characters replaced.
    """
    escape_dict: Dict[str, str] = {
        "\t": "\\t",
        "\n": "\\n",
        "\r": "\\r",
        "\b": "\\b",
        "\f": "\\f",
    }

    for char, escaped in escape_dict.items():
        text = text.replace(char, escaped)
    return text


def echo(message: str) -> str:
    """
    Returns a formatted shell echo command with escaped message text.

    Parameters:
        message (str): The message to format.

    Returns:
        str: The formatted shell echo command.
    """
    return f"echo '{IKEIN_NAME}: {__escape_special_characters(message)}'"


def precho(message: str) -> None:
    """
    Prints a formatted message with escaped characters.

    Parameters:
        message (str): The message to print.
    """
    print(__escape_special_characters(f"{IKEIN_NAME}: {message}"))


def printsh(message: str) -> None:
    """
    Prints a message with escaped characters.

    Parameters:
        message (str): The message to print.
    """
    print(__escape_special_characters(message))


def secure_input(prompt: str) -> str:
    """
    Displays a prompt and securely takes user input, ensuring proper formatting.

    Parameters:
        prompt (str): The input prompt message.

    Returns:
        str: The user input string.
    """
    print(
        __escape_special_characters(f"{IKEIN_NAME}: {prompt}"),
        file=sys.stderr,
        end="",
        flush=True,
    )
    return input()


def confirm(prompt: str) -> bool:
    """
    Displays a confirmation prompt and returns True for 'y' and False otherwise.

    Parameters:
        prompt (str): The confirmation prompt message.

    Returns:
        bool: True if user confirms with 'y', otherwise False.
    """
    print(
        __escape_special_characters(f"{IKEIN_NAME}: {prompt} (y/n): "),
        file=sys.stderr,
        end="",
        flush=True,
    )
    return input().lower() == "y"
