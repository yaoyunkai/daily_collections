"""
使用threadpool的优势是可以获取返回结果


Created at 2023/3/28
"""

import urllib.request
from concurrent.futures import ThreadPoolExecutor
from socket import AF_INET, SOCK_STREAM, socket


def echo_client(sock, client_addr):
    """
    Handle a client connection
    """
    print('Got connection from', client_addr)
    while True:
        msg = sock.recv(65536)
        if not msg:
            break
        sock.sendall(msg)
    print('Client closed connection')
    sock.close()


def echo_server(addr):
    _pool = ThreadPoolExecutor(128)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        _pool.submit(echo_client, client_sock, client_addr)


echo_server(('', 15000))


def fetch_url(url):
    u = urllib.request.urlopen(url)
    data = u.read()
    return data


if __name__ == '__main__':
    pool = ThreadPoolExecutor(10)
    # Submit work to the pool
    a = pool.submit(fetch_url, 'http://www.python.org')
    b = pool.submit(fetch_url, 'http://www.pypy.org')

    # Get the results back
    x = a.result()
    y = b.result()
