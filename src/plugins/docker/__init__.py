from .docker import build_docker_image_tag_and_push

methods = {
    "full": {
        "method": build_docker_image_tag_and_push,
        "info": "Builds a Docker image tag and pushes it to a registry.",
        "usage": "ikein full <server> <image_name> <tag>",
    },
}
