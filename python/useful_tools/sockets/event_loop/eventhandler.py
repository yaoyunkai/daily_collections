"""
事件驱动I/O的一个可能好处是它能处理非常大的并发连接，而不需要使用多线程或多进程。
也就是说，select() 调用（或其他等效的）能监听大量的socket并响应它们中任何一个产生事件的。
在循环中一次处理一个事件，并不需要其他的并发机制。


事件驱动I/O的缺点是没有真正的同步机制。 如果任何事件处理器方法阻塞或执行一个耗时计算，它会阻塞所有的处理进程。
调用那些并不是事件驱动风格的库函数也会有问题，同样要是某些库函数调用会阻塞，那么也会导致整个事件循环停止。

"""

import select


class EventHandler:
    def fileno(self):
        """Return the associated file descriptor"""
        raise NotImplemented('must implement')

    def wants_to_receive(self):
        """Return True if receiving is allowed"""
        return False

    def handle_receive(self):
        """Perform the receive operation"""
        pass

    def wants_to_send(self):
        """Return True if sending is requested"""
        return False

    def handle_send(self):
        """Send outgoing data"""
        pass


def event_loop(handlers):
    while True:
        wants_recv = [h for h in handlers if h.wants_to_receive()]
        wants_send = [h for h in handlers if h.wants_to_send()]
        can_recv, can_send, _ = select.select(wants_recv, wants_send, [])
        for h in can_recv:
            h.handle_receive()
        for h in can_send:
            h.handle_send()
