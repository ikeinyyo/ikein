from .git import create_new_feature_branch

methods = {
    "gnewf": {
        "method": create_new_feature_branch,
        "info": "Creates a new feature branch.",
        "usage": "ikein gnewf [feature_name]",
    },
}
