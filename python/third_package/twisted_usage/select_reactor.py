"""
file: select_reactor.py
Created by Libyao at 2023/4/13

基于select的事件循环


"""

import select


class Reactor:
    def __init__(self):
        self._readers = {}
        self._writers = {}

    def add_reader(self, readable, handler):
        self._readers[readable] = handler

    def add_writer(self, writable, handler):
        self._writers[writable] = handler

    def remove_reader(self, readable):
        self._readers.pop(readable, None)

    def remove_writer(self, writable):
        self._writers.pop(writable, None)

    def run(self):
        while self._readers or self._writers:
            can_read, can_write, _ = select.select(self._readers, self._writers, [])  # blocking
            for r in can_read:
                self._readers[r](self, r)
            for w in can_write:
                if w in self._writers:
                    self._writers[w](self, w)
