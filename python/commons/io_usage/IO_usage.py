"""

IOBase
    BufferedIOBase
        BufferedWriter
        BufferedReader
        BufferedRWPair
        BufferedRandom
        BytesIO
        _SocketWriter

    RawIOBase
        FileIO
        SocketIO

    TextIOBase
        TextIOWrapper
        StringIO

open
    r, a, w -> TextIOWrapper    buffer: BufferedWriter
    rb -> BufferedReader        raw:    FileIO
    wb -> BufferedWriter

BytesIO

在 close() 方法被调用时将会丢弃缓冲区。
只要视图保持存在，BytesIO 对象就无法被改变大小或关闭。

getbuffer
getvalue

seek(offset, whence): 0 开头 1 当前位置 2 末尾位置
readline:    从流中读取并返回一行。如果指定了 size，将至多读取 size 个字节。
             对于二进制文件行结束符总是 b'\n'
truncate     将流的大小调整为给定的 size 个字节（如果未指定 size 则调整至当前位置）。


Created at 2023/3/8
"""


def test():
    f = open('parse_command.py', mode='rb',)
    print(type(f))
    print()

    for k in dir(f):
        if k.startswith('__'):
            continue
        v = getattr(f, k)
        if callable(v):
            continue
        print(k, v)


if __name__ == '__main__':
    test()
