import pickle

from coroutine import coroutine


@coroutine
def sendto(f):
    try:
        while True:
            item = yield
            print(f'dump content: {item}')
            pickle.dump(item, f)
            f.flush()
    except StopIteration:
        f.close()


def recvfrom(f, target):
    try:
        while True:
            print(f)
            item = pickle.load(f)
            target.send(item)
    except EOFError:
        target.close()


if __name__ == '__main__':
    import xml.sax

    from cosax import EventHandler
    from buses import buses_to_dicts

    import subprocess

    p = subprocess.Popen(['python', 'busproc.py'], stdin=subprocess.PIPE)

    xml.sax.parse("tiny_routes.xml", EventHandler(buses_to_dicts(sendto(p.stdin))))
