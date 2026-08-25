from typing import List

from utils.bash import echo


def build_docker_image_tag_and_push(*args: List[str]) -> str:
    """
    Builds a Docker image tag and pushes it to a registry.

    Parameters:
        args (List[str]): The list of arguments, which should include the server, image name, and tag.

    Returns:
        str: A message indicating the result of the operation.

    """

    if len(args) == 3:
        return f"""
        docker buildx build --platform linux/amd64 -t {args[0]}/{args[1]}:{args[2]} --push .
        """
    return echo(
        "Invalid number of arguments. Server, image name, and tag are required."
    )
