# cothread.py
#
# A thread object that runs a coroutine inside it.  Messages get sent
# via a Queue object

from queue import Queue
from threading import Thread


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr

    return start


def threaded(target):
    messages = Queue()

    def run_target():
        while True:
            item_in = messages.get()
            if item_in is GeneratorExit:
                target.close()
                return
            else:
                target.send(item_in)

    Thread(target=run_target).start()
    try:
        while True:
            item = (yield)
            messages.put(item)
    except GeneratorExit:
        messages.put(GeneratorExit)
