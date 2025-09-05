"""

use Queue for Generator from threads

"""


def genfrom_queue(the_queue):
    while True:
        item = the_queue.get()
        if item is StopIteration:
            break
        yield item


def sendto_queue(items, the_queue):
    for item in items:
        the_queue.put(item)
    the_queue.put(StopIteration)
