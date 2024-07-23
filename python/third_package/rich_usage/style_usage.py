"""
https://rich.readthedocs.io/en/latest/appendix/colors.html#appendix-colors


三种用法

1. string
2. style class
3. style theme


Created at 2024/7/22
"""

from rich.console import Console
from rich.style import Style
from rich.theme import Theme

console = Console()

console.print("DANGER!", style="red on white")
console.print("Danger, Will Robinson!", style="blink bold red underline on white")

danger_style = Style(color="red", blink=True, bold=True)
console.print("Danger, Will Robinson!", style=danger_style)


# Theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console = Console(theme=custom_theme)
console.print("This is information", style="info")
console.print("[warning]The pod bay doors are locked[/warning]")
console.print("Something terrible happened!", style="danger")
