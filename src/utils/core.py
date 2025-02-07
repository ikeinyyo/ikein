from .bash import printsh


def list_methods(ikein_info):
    for category in ikein_info:
        printsh(f"- {category}")
        for method in ikein_info[category]:
            printsh(f"\t- {method}: {ikein_info[category][method]['info']}")
    return ""


methods = {
    "ikein": {"list": {"method": list_methods, "info": "Show all ikein options"}}
}
