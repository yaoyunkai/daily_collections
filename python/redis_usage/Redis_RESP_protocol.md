# RESP protocol spec

RESP可以序列化不同的数据类型，如整数、字符串和数组。还有一种特定类型的错误。请求以字符串数组的形式从客户端发送到Redis服务器，这些字符串数组表示要执行的命令的参数。Redis使用特定于命令的数据类型进行回复。

RESP是二进制安全的，不需要处理从一个进程传输到另一个进程的大量数据，因为它使用前缀长度来传输大量数据。

## 请求-响应模型

Redis接受由不同参数组成的命令。接收到命令后，将对其进行处理，并将回复发送回客户端。

- Redis支持流水线(本文稍后将介绍)。因此，客户端可以一次发送多个命令，然后等待回复。
- 当Redis客户端订阅一个Pub/Sub通道时，协议改变语义，成为一个推送协议。客户端不再需要发送命令，因为一旦收到新消息，服务器就会自动向客户端(对于客户端订阅的通道)发送新消息。

## protocol description

RESP实际上是一种序列化协议，支持以下数据类型:简单字符串、错误、整数、批量字符串和数组。

Redis以以下方式使用RESP作为请求-响应协议:

- 客户端发送命令到Redis服务器作为一个RESP arrays 的 bulk string。
- 服务器根据命令实现使用其中一种RESP类型进行应答。

在RESP中，第一个字节决定数据类型:

- **Simple Strings**, `+`
- **Errors**, `-`
- **Integers**, `:`
- **Bulk Strings**, `$`
- **Arrays**, `*`

在RESP中，协议的不同部分总是以“\r\n”(CRLF)结束。

### simple string

```
"+OK\r\n"
```

当Redis响应一个简单字符串时，客户端库应该响应一个由'+'之后的第一个字符组成的字符串，直到字符串的结尾，不包括最后的CRLF字节。

### response error

RESP对错误有特定的数据类型。它们类似于RESP简单字符串，但第一个字符是减号“-”字符而不是加号。RESP中简单字符串和错误之间的真正区别在于客户端将错误视为异常，而组成Error类型的字符串就是错误消息本身。

```
"-Error message\r\n"

-ERR unknown command 'helloworld'
-WRONGTYPE Operation against a key holding the wrong kind of value
```

客户端实现可以为不同的错误返回不同类型的异常，或者通过直接将错误名称作为字符串提供给调用者来提供一种通用的捕获错误的方法。

### integers

This type is just a CRLF-terminated string that represents an integer, prefixed by a ":" byte. For example, `":0\r\n"` and `":1000\r\n"` are integer replies.

### bulk string

Bulk Strings are encoded in the following way:

- A "$" byte followed by the number of bytes composing the string (a prefixed length), terminated by CRLF.
- The actual string data.
- A final CRLF.

```
"$5\r\nhello\r\n"

"$0\r\n\r\n"  --> blank string

"$-1\r\n"  --> NULL
```

###  arrays

客户端使用RESP阵列向Redis服务器发送命令。类似地，某些Redis命令，返回元素的集合到客户端，使用RESP数组作为他们的回复。一个例子是返回列表元素的LRANGE命令。

RESP Arrays are sent using the following format:

- A `*` character as the first byte, followed by the number of elements in the array as a decimal number, followed by CRLF.
- An additional RESP type for every element of the Array.

```
"*0\r\n"  blank array

"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n"

```

## 发送命令

