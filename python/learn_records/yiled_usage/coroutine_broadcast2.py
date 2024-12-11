import time


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr

    return start


def follow(thefile, target):
    thefile.seek(0, 2)  # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)  # Sleep briefly
            continue
        target.send(line)


# A filter.
@coroutine
def grep(pattern, target):
    while True:
        line = (yield)  # Receive a line
        if pattern in line:
            target.send(line)  # Send to next stage


# A sink.  A coroutine that receives data
@coroutine
def printer():
    while True:
        line = (yield)
        print(line)


# Broadcast a stream onto multiple targets
@coroutine
def broadcast(targets):
    while True:
        item = (yield)
        for target in targets:
            target.send(item)


# Example use
if __name__ == '__main__':
    f = open("access-log")
    p = printer()
    follow(f, broadcast([grep('python', p),
                         grep('ply', p),
                         grep('swig', p)]))
