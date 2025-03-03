import re
import sys

IKEIN_NAME = "- [I.K.E.I.N.]"


def __escape_special_characters(text):
    escape_dict = {
        "\t": "\\t",
        "\n": "\\n",
        "\r": "\\r",
        "\b": "\\b",
        "\f": "\\f",
    }

    for char, escaped in escape_dict.items():
        text = text.replace(char, escaped)
    return text


def echo(message: str):
    return f"echo '{IKEIN_NAME}: {__escape_special_characters(message)}'"


def precho(message: str):
    print(__escape_special_characters(f"{IKEIN_NAME}: {message}"))


def printsh(message: str):
    print(__escape_special_characters(message))


def secure_input(prompt):
    print(
        __escape_special_characters(f"{IKEIN_NAME}: {prompt}"),
        file=sys.stderr,
        end="",
        flush=True,
    )
    return input()


def confirm(prompt):
    print(
        __escape_special_characters(f"{IKEIN_NAME}: {prompt} (y/n): "),
        file=sys.stderr,
        end="",
        flush=True,
    )
    return input().lower() == "y"
