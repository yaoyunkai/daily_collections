"""
Console

size
encoding
is_terminal
color_system

print
log
out

# 旋转动画
with console.status("Working..."):
    do_work()


from rich.json import JSON



--------------------------------------------------------------------------

chcp
    https://learn.microsoft.com/en-us/windows/win32/intl/code-page-identifiers

尝试 cmd 和 终端的不同, 和 idea里面的输出有什么不同
check the encoding use the Rich

Created at 2024/7/22
"""
from typing import List

from rich import inspect
from rich.console import Console, OverflowMethod
from rich.terminal_theme import MONOKAI


def run_console_apis():
    console = Console()

    inspect(console, )
    console.print([1, 2, 3])
    console.print("[blue underline]Looks like a link, ssss [/blue underline] this is the end of line")
    console.print(locals())
    console.print("FOO", style="white on blue")

    # console.log("Hello, World!")

    console.print_json('[false, true, null, "foo"]')

    # lower-level output
    console.out("Locals", locals())

    console.rule("[bold red]Chapter 2", characters='~')


def run_console_apis2():
    console = Console(width=20)

    style = "bold white on blue"
    console.print("Rich", style=style)
    console.print("Rich", style=style, justify="left")
    console.print("Rich", style=style, justify="center")
    console.print("Rich", style=style, justify="right")


def run_console_overflow():
    console = Console(width=14)
    supercali = "supercalifragilisticexpialidocious"

    overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
    for overflow in overflow_methods:
        console.rule(overflow)
        console.print(supercali, overflow=overflow, style="bold blue")
        console.print()


def run_console_style():
    blue_console = Console(style="white on blue")
    blue_console.print("I'm blue. Da ba dee da ba di.")


def run_console_export():
    console = Console(record=True)
    console.print([1, 2, 3])
    console.print("[blue underline]Looks like a link, ssss [/blue underline] this is the end of line")
    console.print(locals())
    console.print("FOO", style="white on blue")

    console.save_svg("example.svg", theme=MONOKAI)


if __name__ == '__main__':
    # run_console_apis()
    # run_console_apis2()
    # run_console_overflow()
    # run_console_style()

    run_console_export()
