#
# A thread object that runs a coroutine inside it.  Messages get sent
# via a Queue object
import xml.sax
from queue import Queue
from threading import Thread

from buses import bus_locations, buses_to_dicts, filter_on_field
from coroutine import coroutine
from cosax import EventHandler


@coroutine
def threaded(target):
    messages = Queue()

    def run_target():
        while True:
            _item = messages.get()
            if _item is GeneratorExit:
                target.close()
                return
            else:
                target.send(_item)

    Thread(target=run_target).start()
    try:
        while True:
            item = yield
            messages.put(item)
    except GeneratorExit:
        messages.put(GeneratorExit)


if __name__ == '__main__':
    co = filter_on_field('direction', 'North Bound', bus_locations())

    xml.sax.parse("tiny_routes.xml", EventHandler(buses_to_dicts(threaded(co))))
