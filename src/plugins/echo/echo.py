from utils.bash import echo
from utils.config import get_config


def say_hello(*args):
    if len(args):
        return echo(f"Hi {args[0]}")
    return echo(f"Hi {get_config().get('displayName', '')}!")
