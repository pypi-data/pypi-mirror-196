from thonny import get_workbench
from thonny.workbench import SyntaxThemeSettings


def monokai() -> SyntaxThemeSettings:
    bg = "#272822"
    bg_light = "#363636"
    fg = "#fdfff1"
    comment = "#6e7066"
    comment_light = "#c0c1b5"
    red = "#f92672"
    green = "#a6e22e"
    yellow = "#e6db74"
    orange = "#fd971f"
    blue = "#66d9ef"
    magenta = "#ae81ff"
    white = "#eeeeee"

    return {
        "TEXT": {"foreground": fg, "insertbackground": fg, "background": bg},
        "GUTTER": {"foreground": comment_light, "background": bg},
        "breakpoint": {"foreground": red},
        "current_line": {"background": bg_light},
        "sel": {"foreground": "", "background": bg_light},
        "definition": {"foreground": blue},
        "class_definition": {"foreground": blue, "range": green},
        "function_definition": {"foreground": green},
        "string": {"foreground": yellow},
        "string3": {"foreground": comment},
        "open_string": {"foreground": yellow, "background": bg_light},
        "open_string3": {"foreground": orange, "background": bg_light},
        "tab": {"background": bg},
        "builtin": {"foreground": blue},
        "keyword": {"foreground": red},
        "number": {"foreground": magenta},
        "comment": {"foreground": comment},
        "welcome": {"foreground": blue},
        "magic": {"foreground": red},
        # shell
        "prompt": {"foreground": blue},
        "stdin": {"foreground": yellow},
        "stdout": {"foreground": white},
        "stderr": {"foreground": red},
        "value": {"foreground": yellow},
        "function_call": {"foreground": green},
        "method_call": {"foreground": green},
        "hyperlink": {"foreground": blue},
        # paren matcher
        "surrounding_parens": {"foreground": red},
        "unclosed_expression": {"background": bg_light},
    }


def load_plugin() -> None:
    get_workbench().add_syntax_theme("Monokai", "Default Dark", monokai)
