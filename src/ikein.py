import sys

from utils.loads import load


def main(ikein_info, ikein_methods, methods, args):
    command = args[1]
    try:
        if command in ikein_methods:
            output_command = ikein_methods[command]["method"](ikein_info)
        else:
            output_command = methods[command]["method"](*args[2:])

        print(output_command)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    ikein_info, ikein_methods, methods = load("plugins")
    main(ikein_info, ikein_methods, methods, sys.argv)
