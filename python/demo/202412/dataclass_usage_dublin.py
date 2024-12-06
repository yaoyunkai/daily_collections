"""


created at 2024/12/6
"""
from dataclasses import dataclass, field
from datetime import date
from enum import Enum, auto
from typing import Optional


class ResourceType(Enum):
    BOOK = auto()
    EBOOK = auto()
    VIDEO = auto()


@dataclass
class Resource:
    identifier: str
    title: str = '<untitled>'
    creators: list[str] = field(default_factory=list)
    date: Optional[date] = None

    type: ResourceType = ResourceType.BOOK
    description: str = ''
    language: str = ''
    subjects: list[str] = field(default_factory=list)


if __name__ == '__main__':
    desc = "Improving the design of existing code"
    book = Resource('978-0-13-475759-9',
                    'Refactoring, 2nd Edition',
                    ['Martin Fowler', 'Kent Beck'],
                    date(2018, 11, 19),
                    ResourceType.BOOK,
                    desc,
                    'EN',
                    ['computer programming', 'OOP'])

    print(book)
