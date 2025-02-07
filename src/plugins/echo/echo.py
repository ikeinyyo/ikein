from utils.bash import echo


def say_hello(*args):
    if len(args):
        return echo(f"Hi {args[0]}")
    return echo("Hi")
