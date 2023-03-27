"""
在创建一个类的对象时，如果之前使用同样参数创建过这个对象， 你想返回它的缓存引用。

Created at 2023/3/27
"""
import threading
import weakref


class Spam:
    def __init__(self, name):
        self.name = name


_spam_cache = weakref.WeakValueDictionary()
_lock = threading.RLock()


def _get_spam(name):
    if name not in _spam_cache:
        s = Spam(name)
        _spam_cache[name] = s
    else:
        s = _spam_cache[name]

    return s


def get_spam(name):
    with _lock:
        return _get_spam(name)


# ----------------------------------------------------------------


class CachedSpam2Manager:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            s = Spam(name)
            self._cache[name] = s
        else:
            s = self._cache[name]
        return s

    def clear(self):
        self._cache.clear()


class Spam2:
    manager = CachedSpam2Manager()

    def __init__(self, name):
        self.name = name


def get_spam2(name):
    return Spam2.manager.get_spam(name)


if __name__ == '__main__':
    a = get_spam('foo')
    b = get_spam('bar')
    c = get_spam('foo')

    print(a == b)
    print(a == c)
