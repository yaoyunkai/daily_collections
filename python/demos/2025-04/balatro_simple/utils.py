"""


created at 2025/4/18
"""

import threading

__all__ = [
    'print_noun', 'IdGenerator',
]


def print_noun(noun_val: str, numbers: int):
    if numbers > 1:
        noun_val = '{}s'.format(noun_val)
    return f'{numbers} {noun_val}'


class _InternalID:

    def __init__(self):
        self._next_id = 0
        self._lock = threading.Lock()

    def get_next_id(self):
        with self._lock:
            val = self._next_id
            self._next_id += 1
            return val


IdGenerator = _InternalID()
