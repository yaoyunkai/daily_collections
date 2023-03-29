"""


Created at 2023/3/28
"""

import threading


class SharedCounter:
    """
    A counter object that can be shared by multiple threads.
    """

    def __init__(self, initial_value=0):
        self._value = initial_value
        self._value_lock = threading.Lock()

    def incr(self, delta=1):
        """
        Increment the counter with locking
        """
        self._value_lock.acquire()
        self._value += delta
        self._value_lock.release()

    def decr(self, delta=1):
        """
        Decrement the counter with locking
        """
        self._value_lock.acquire()
        self._value -= delta
        self._value_lock.release()


class SharedCounter2:
    """
    A counter object that can be shared by multiple threads.
    """
    _lock = threading.RLock()

    def __init__(self, initial_value=0):
        self._value = initial_value

    def incr(self, delta=1):
        """
        Increment the counter with locking
        """
        with SharedCounter2._lock:
            self._value += delta

    def decr(self, delta=1):
        """
        Decrement the counter with locking
        """
        with SharedCounter2._lock:
            self.incr(-delta)
