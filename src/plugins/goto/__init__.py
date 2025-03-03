from .goto import goto

methods = {
    "goto": {
        "method": goto,
        "info": "Manage and navigate to predefined directory aliases.",
        "usage": "ikein goto [-a <alias> <directory>] | [<alias>] | [-l] | [-o <alias>] | [-r <alias>]",
    }
}
