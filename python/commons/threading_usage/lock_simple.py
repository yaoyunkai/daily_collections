"""
Threading Lock
    acquire
    release
    locked



Created at 2023/2/18
"""
import threading


def test_release():
    lock = threading.Lock()
    print(lock.locked())

    lock.release()
    lock.acquire()
    lock.release()


if __name__ == '__main__':
    test_release()
