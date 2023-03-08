# Redis 

## Python IO 层次结构

```
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

```

