"""

BaseException


Redis.__init__
    ConnectionPool
    response_callbacks ->

    connection = None or SSLConnection

        health_check_interval = 0

        self.socket_timeout = None
        self.socket_connect_timeout = None
        self.socket_keepalive = False
        self.socket_keepalive_options = {}

        pid
        encoder : 两个参数控制编码 encoding 控制写入, decode_responses 控制输出是否解码
        _sock

        _parser PythonParser -> BaseParser
            _sock
            _buffer  SocketBuffer
                    self._sock = socket
                    self.socket_read_size = socket_read_size
                    self.socket_timeout = socket_timeout
                    self._buffer = io.BytesIO()
                        readline : 读取一行
                        seek: 移动流的位置
                        tell: 返回流的位置
                        write: 写入数据

                        readline write: 都会移动流的指针
                        BytesIO.seek 将流位置修改到给定的字节 offset 默认开头

                    self.bytes_written = 0
                    self.bytes_read = 0

            encoder -> connection.encoder

        connect

            _connect : create TCP socket
                socket.getaddrinfo  DNS ?

                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) TCP nodelay
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)   keep alive
                sock.setsockopt(socket.IPPROTO_TCP, k, v)

                sock.settimeout: None 阻塞  0表示非阻塞 非负数表示阻塞多少秒之后超时

                sock.connect
                sock.send_all()  成功后会返回 None。出错后会抛出一个异常，
                sock.shutdown  SHUT_RDWR  则后续的发送和接收都不允许
                sock.close     如果需要及时关闭连接，请在调用 close() 之前调用 shutdown()。

            on_connect
                self._parser.on_connect

        pack_command: 转换命令为 RESP 协议



    ConnectionPool
        pid -> process id
        _fork_lock   Lock
        _lock        RLock
        self._created_connections = 0  记录连接的数量
        self._available_connections = []
        self._in_use_connections = set()

        all in _lock

        get_connection
            make_connection : 创建一个Connection object

        release: return conn instance to available_pool

    execute_command:
        connection. send_command

    parse_response:
        connection. read_response ->
            _parser. read_response ->
                buffer.readline
                SocketBuffer
                    self.bytes_written = 0  从socket中读入的buf
                    self.bytes_read = 0    从 buf 中已经读了的

                    length: bytes_written - bytes_read

                    _read_from_socket

                    can_read
                    read
                    readline
                    purge
                    close

        response_callbacks[command_name](response, **options)

------------------------------------------------------------------------------------

redis 序列化协议: https://redis.io/docs/latest/develop/reference/protocol-spec/

本质就是 type length data   ->>>>> $ *
        type data          ->>>>>  - + :

$<length>\r\n<data>\r\n

-  error
+  simple string
:  integer
*  array
$  bulk string


read_response:
    $ 会使用 Parser 的 read



SocketBuffer
    readline:
        seek byte_read

        read buf
            read socket

        read from socket: seek byte_writen at start
                          write data to buf
                          update byte_writen


    read


TextIOWrapper



Created at 2024/7/23
"""

import redis


def test_get_addr():
    """
    (<AddressFamily.AF_INET6: 23>, <SocketKind.SOCK_STREAM: 1>, 0, '', ('2600:1406:2e00:390::1aca', 443, 0, 0))
    (<AddressFamily.AF_INET6: 23>, <SocketKind.SOCK_STREAM: 1>, 0, '', ('2600:1406:2e00:3a5::1aca', 443, 0, 0))
    (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 0, '', ('23.221.77.22', 443))

    """
    import socket

    for res in socket.getaddrinfo('www.apple.com', 443, 0, socket.SOCK_STREAM):
        print(res)


if __name__ == '__main__':
    conn = redis.Redis(db=0, encoding='utf8', decode_responses=True)
    # conn.set('name', 'tom\nwelcome'.encode('utf8'))

    conn.get('name')

    arr = conn.lrange('arr1', 0, -1)
    print(arr)

    length = conn.llen('arr1')

    conn.close()

    # test_get_addr()

    # f = open('pubsub.py', mode='a')
    # f.close()
    #
    # print(f.__class__)
