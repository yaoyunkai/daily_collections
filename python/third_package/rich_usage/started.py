"""
Console Markup

inspect 查看一个object ?




Created at 2024/7/22
"""

import datetime

from rich import inspect
from rich import print
from rich.color import Color

print("[italic red]Hello[/italic red] World!", locals())

color = Color.parse("red")
inspect(color, methods=True)

inspect(datetime.datetime.now(), methods=True)
