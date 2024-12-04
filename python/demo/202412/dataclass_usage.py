"""


created at 2024/12/4
"""

from dataclasses import InitVar
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class ClubMember:
    all_handles: ClassVar[set[str]] = set()

    name: str
    level: int
    guests: list[str] = field(default_factory=list)
    athlete: bool = field(default=False, repr=False)
    handle: str = ''

    def __post_init__(self):
        pass


@dataclass
class Foo:
    """
    仅做初始化的变量
    对于生成的__init__方法，database是参数之一，同时也传给__post_init__方法。

    """
    i: int
    j: int = None
    database: InitVar = None

    def __post_init__(self, database):
        if self.j is None and database is not None:
            self.j = database.lookup('j')


if __name__ == '__main__':
    c = ClubMember('tom', 23)
    c.guests.append('sdf')
