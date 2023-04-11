"""


Created at 2023/4/11
"""
import selectors
import socket

selector = selectors.DefaultSelector()

urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}


class Stopped:
    stop = False


class Future:
    """
    未来对象
    异步调用执行完的时候，就把结果放在它里面。
    """

    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        # print('self callback: ', self._callbacks)
        for fn in self._callbacks:
            fn(self)


class Crawler:
    def __init__(self, url_addr):
        self.url = url_addr
        self.response = b''

    def fetch(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)

        try:
            sock.connect(('localhost', 9000))
        except BlockingIOError:
            pass

        f = Future()

        def on_connect():
            f.set_result(None)

        selector.register(sock.fileno(), selectors.EVENT_WRITE, on_connect)
        yield f

        selector.unregister(sock.fileno())
        get = 'GET {0} HTTP/1.0 \r\nHost: example.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('utf8'))

        while True:
            f = Future()

            def on_readable():
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(), selectors.EVENT_READ, on_readable)
            chunk = yield f
            print('get self: {} chunk: {}'.format(self.url, chunk))
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                print(urls_todo)
                try:
                    urls_todo.remove(self.url)
                except Exception:
                    pass
                if not urls_todo:
                    Stopped.stop = True
                    break


class Task:
    """任务对象"""

    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            # send放到coro执行，即fetch，直到下次yield
            # next_future为yield返回对象
            next_future = self.coro.send(future.result)
        except StopIteration:
            return

        # 等待下一次 set_result 继续执行
        next_future.add_done_callback(self.step)


def loop():
    while not Stopped.stop:

        events = selector.select()
        for ek, em in events:
            print('get event: ', ek.fd, ', event type:', em)

            callback = ek.data

            # 用事件来驱动 Future调用 set_result
            callback()


if __name__ == '__main__':
    import time

    start = time.time()
    for url in urls_todo:
        crawler = Crawler(url)

        # 这里已经运行到register event了
        Task(crawler.fetch())
    loop()
    print(time.time() - start)
