"""
generators.py

生成器模式


:=
在一个表达式内部，同时完成“为变量赋值”和“返回该变量的值”两个操作。

created at 2026-05-19
"""

import os
from typing import Iterable, Iterator, TypedDict


class LogRecord(TypedDict):
    level: str
    message: str


def lines_from_file(filepath: str | os.PathLike[str]) -> Iterator[str]:
    with open(filepath, mode="r") as fp:
        for line in fp:
            yield line.rstrip("\n")


def matching_lines(lines: Iterable[str], pattern: str) -> Iterator[str]:
    for line in lines:
        if pattern in line:
            yield line


def matching_lines_from_file(filepath: str | os.PathLike[str], pattern: str) -> Iterator[str]:
    # with open(filepath, mode="r") as handle:
    #     while (line := handle.readline()) != "":
    #         if pattern in line:
    #             # "{line!r}"
    #             yield line.rstrip("\n")

    yield from matching_lines(lines_from_file(filepath), pattern)


def parse_log_records(log_lines: Iterable[str]) -> Iterator[LogRecord]:
    for line in log_lines:
        level, message = line.split(": ", 1)
        yield LogRecord(level=level, message=message)


def words_in_text(lines: Iterable[str]):
    for line in lines:
        for word in line.split():
            yield word


def house_records(lines: Iterable[str]):
    record = {}
    for line in lines:
        if line == "":
            yield record
            record = {}
            continue
        key, value = line.split(": ", 1)
        record[key] = value
    yield record


if __name__ == "__main__":
    for d in house_records(lines_from_file("data1.txt")):
        print(d)
