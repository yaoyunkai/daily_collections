Paramiko

Paramiko is a pure-Python 1 (3.6+) implementation of the SSHv2 protocol 2,
providing both client and server functionality.

https://www.iana.org/assignments/ssh-parameters/ssh-parameters.xhtml

paramiko.Transport(('localhost', 22))


-----------------------------------------------------------------------------------------------------------------------
Client

SSHClient
    先建立TCP 连接
    初始化 Transport
    设置 Transport的一些参数
    transport.start_client()
    self._auth()


exec_command:
    open_session

    open_channel



-----------------------------------------------------------------------------------------------------------------------
Channel






-----------------------------------------------------------------------------------------------------------------------
Transport

__init__
    sock. timeout -> 0.1s
    初始化 Packetizer
    _channels 是一个 ChannelMap()


start_client:
    两种方式 同步和异步
    threading start 启动一个新的线程

    start -> run

run:

    send local_version -> write_all  --> SSH-2.0-paramiko_2.12.0\r\n
    check banner

    start_handshake
    _send_kex_init

    _expect_packet

    ptype, m = self.packetizer.read_message()



_check_banner
    call packet readline for get data

    ----> SSH-2.0-OpenSSH_7.4

    匹配 version 和 client (server)


_send_kex_init:
    和服务器协商一个什么东西?  交换加密算法和密钥

    构造了一个 Message对象
    call packet._send_message


_expect_packet:
    kex obj用于注册它期望看到的下一个数据包类型。


open_session:


open_channel:
    初始化一个 Channel


_send_user_message: 发个消息，但在关键谈判时阻止。这用于用户发起的请求。



-----------------------------------------------------------------------------------------------------------------------
Message
Implementation of an SSH2 "message".





-----------------------------------------------------------------------------------------------------------------------
Packetizer

    Implementation of the base SSH packet protocol.


write_all
    call send -> 分段发送数据到remote sock
    https://docs.python.org/zh-cn/3/library/socket.html#socket.socket.send


readline
    linefeed_byte: \n of bytes

    先假设 self.__remainder 是空
    从sock中读取数据直到遇到\n 写入到 __remainder
    读取到的放到 buf

    将 \n 之前的数据返回


_read_timeout : 真正的读取动作
    sock.recv


start_handshake:
    让 __timer_expired 在指定时间后变为True


_send_message:
    data: 从caller传过来的
    cmd: 控制协议

    packet = self._build_packet(data)

    在 write all 会有一个加密动作
    self.write_all(out)


read_message:

    read_all

    ptype, msg: Message


_build_packet:
    给要send的message加上一些填充bytes



read_all:
