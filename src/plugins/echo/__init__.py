from .echo import repeat, say_hello

methods = {
    "echo": {
        "method": repeat,
        "info": "Prints a message.",
        "usage": "ikein echo <message>",
    },
    "hello": {
        "method": say_hello,
        "info": "Prints a greeting message.",
        "usage": "ikein hello",
    },
}
