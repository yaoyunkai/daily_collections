"""


Created at 2023/4/11
"""
import selectors
import socket

selector = selectors.DefaultSelector()

urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}


class Stopped:
    stop = False


class Crawler:

    def __init__(self, url_addr):
        self.url = url_addr
        self.sock = None
        self.response = b''

    def fileno(self):
        return self.sock.fileno()

    def fetch(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)

        try:
            self.sock.connect(('localhost', 9000))
        except BlockingIOError:
            pass
        selector.register(self, selectors.EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        selector.unregister(self)
        get = 'GET {0} HTTP/1.0\r\nHost: example.com\r\n\r\n'.format(self.url)
        self.sock.send(get.encode('ascii'))
        selector.register(self, selectors.EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        # 如果响应大于4kb，下次循环继续
        chunk = self.sock.recv(4096)
        print(chunk)
        if chunk:
            self.response += chunk
        else:
            selector.unregister(self)
            print('xxxxxxxxxxxxxxxxxx')
            print(urls_todo)
            urls_todo.remove(self.url)
            print(urls_todo)
            if not urls_todo:
                print('want to --------------')
                Stopped.stop = True


def loop():
    while not Stopped.stop:
        events = selector.select()  # blocking
        for event_key, event_mask in events:
            print('get event: ', event_key.fd, event_mask)
            callback = event_key.data
            callback(event_key, event_mask)


if __name__ == '__main__':
    import time

    start = time.time()
    for url in urls_todo:
        crawler = Crawler(url)
        crawler.fetch()
    loop()
    print(time.time() - start)
