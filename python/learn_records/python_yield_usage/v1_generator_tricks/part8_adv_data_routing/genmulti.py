"""

Generator 多路复用

example:
    log1 = follow(open("foo/access-log"))
    log2 = follow(open("bar/access-log"))
    lines = multiplex([log1,log2])


"""
import queue
import threading


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


def gen_cat(sources):
    for src in sources:
        yield from src


def multiplex(sources):
    in_q = queue.Queue()
    consumers = []
    for src in sources:
        t = threading.Thread(target=sendto_queue, args=(src, in_q))
        t.start()
        consumers.append(genfrom_queue(in_q))

    return gen_cat(consumers)


def gen_multiplex(genlist):
    item_q = queue.Queue()

    def run_one(source):
        for _item in source:
            item_q.put(_item)

    def run_all():
        thrlist = []
        for source in genlist:
            t = threading.Thread(target=run_one, args=(source,))
            t.start()
            thrlist.append(t)
        for t in thrlist:
            t.join()
        item_q.put(StopIteration)

    threading.Thread(target=run_all).start()
    while True:
        item = item_q.get()
        if item is StopIteration:
            return
        yield item
