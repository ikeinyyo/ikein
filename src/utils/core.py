from .bash import printsh


def list_methods(ikein_info):
    for category in ikein_info:
        printsh(f"- {category}")
        for method in ikein_info[category]:
            printsh(f"\t- {method}: {ikein_info[category][method]['info']}")
    return ""


def usage_method(ikein_info, *args):
    for category in ikein_info:
        for method in ikein_info[category]:
            if method == args[0]:
                printsh(f"- {ikein_info[category][method]['info']}:")
                printsh(f"\t$ {ikein_info[category][method]['usage']}")
    return ""


methods = {
    "ikein": {
        "list": {
            "method": list_methods,
            "info": "Displays all available IKEIN commands.",
            "usage": "ikein list",
        },
        "usage": {
            "method": usage_method,
            "info": "Provides usage details for a specific command.",
            "usage": "ikein usage [command]",
        },
    }
}
