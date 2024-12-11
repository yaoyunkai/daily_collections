# Python Server Hierarchy

```
* RFC 7231: Hypertext Transfer Protocol (HTTP/1.1), obsoletes 2616
* RFC 6585: Additional HTTP Status Codes
* RFC 3229: Delta encoding in HTTP
* RFC 4918: HTTP Extensions for WebDAV, obsoletes 2518
* RFC 5842: Binding Extensions to WebDAV
* RFC 7238: Permanent Redirect
* RFC 2295: Transparent Content Negotiation in HTTP
* RFC 2774: An HTTP Extension Framework
* RFC 7540: Hypertext Transfer Protocol Version 2 (HTTP/2)
```

## BaseServer

所有server的基类，仅提供基本方法和框架，不提供实现：

```
Methods for the caller:
    - __init__(server_address, RequestHandlerClass)
    - serve_forever(poll_interval=0.5)
    - shutdown()
    - handle_request()  # if you do not use serve_forever()
    - fileno() -> int   # for selector
    
```

方法之间的调用：

```
func: server_forever
	register selector
	
	while True:
		ready = select.select
		if ready:
			_handle_request_noblock
		service_actions

func: handle_request: 仅处理一次请求

func: _handle_request_noblock
	request, client_address = self.get_request()
	if self.verify_request(request, client_address):
		process_request
	
	If Error: handle_error 
	          shutdown_request

func: process_request:
	finish_request:
		new ReuqestHandleClass for every request:
		    def __init__(self, request, client_address, server):
                self.request = request
                self.client_address = client_address
                self.server = server
                self.setup()
                try:
                    self.handle()
                finally:
                    self.finish()
	shutdown_request:
		close_request
```

## TCPServer

主要逻辑多了一些对socket的处理：

```
__init__:   		socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_bind: 		socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse
		     		socket.bind(self.server_address)
             		server_address = self.socket.getsockname()
             		
server_activate:    socket.listen(self.request_queue_size) 
server_close:       socket.close()
fileno:             socket.fileno()

get_request:        socket.accept()
shutdown:           socket.shutdown(socket.SHUT_WR)
```

## ThreadingMixIn

```python
def process_request(self, request, client_address):
    """Start a new thread to process the request."""
    t = threading.Thread(target = self.process_request_thread,
                         args = (request, client_address))
    t.daemon = self.daemon_threads
    if not t.daemon and self.block_on_close:
        if self._threads is None:
            self._threads = []
        self._threads.append(t)
    t.start()

def server_close(self):
    super().server_close()
    if self.block_on_close:
        threads = self._threads
        self._threads = None
        if threads:
            for thread in threads:
                thread.join()
```

## http site

- HTTPServer
- ThreadingHTTPServer

RequesthandlerClass Hierarchy:

```
BaseRequestHandler (socketserver stub)
    StreamRequestHandler(BaseRequestHandler) (socketserver stub)
        BaseHTTPRequestHandler(socketserver.StreamRequestHandler) (http.server)
            SimpleHTTPRequestHandler(BaseHTTPRequestHandler) (http.server)
                CGIHTTPRequestHandler(SimpleHTTPRequestHandler) (http.server)
                
```

IO Hierarchy:

[io处理流的核心工具](https://docs.python.org/zh-cn/3/library/io.html)

- RawIOBase
- BufferedIOBase
- TextIOBase

```
IOBase (io stub)
    RawIOBase(IOBase) (io stub)
        SocketIO(RawIOBase) (socket stub)

IOBase (io stub)
    BufferedIOBase(IOBase) (io stub)
        BufferedWriter(BufferedIOBase, BinaryIO) (io stub)
            BufferedRandom(BufferedReader, BufferedWriter) (io stub)
```

RequestHandlerClass:

```
connection: request socket
rfile: io.BufferedReader(raw, 8192) raw: SocketIO(self, 'r')
wfile: SocketIO(self, 'w')  -> _SocketWriter(BufferedIOBase)
```

处理逻辑：

```
func handle
	self.close_connection
	handle_one_request
	while not close_connection:
		handle_one_request

func: handle_one_request
	
```

## WSGI Protocol

**WSGIServer** 有如下两种Handler:

1, WSGI的ServerHandler:

```
BaseHandler (wsgiref.handlers stub)
    SimpleHandler(BaseHandler) (wsgiref.handlers stub)
        ServerHandler(SimpleHandler) (wsgiref.simple_server)

```

RequestHandler 与 ServerHandler交互：

```python
handler = ServerHandler(
        self.rfile, self.wfile, self.get_stderr(), self.get_environ()
    )
handler.request_handler = self      # backpointer for logging
handler.run(self.server.get_app())
```

2, RequestHandler 每个请求会实例化一次。

```
BaseHTTPRequestHandler.parse_request:
	self.raw_requestline
	self.requestline: 'GET / HTTP/1.1'
	self.requestversion: 'HTTP/1.1'
	self.command GET
	self.path /
	self.headers: HTTPMessage

```

## Django Dev Server

```
Django Dev Simple Server:

Server class: WSGIServer(simple_server.WSGIServer)

RequestHandlerClass: WSGIRequestHandler(simple_server.WSGIRequestHandler)
    request handler 委派 ServerHandler(simple_server.ServerHandler) 处理请求

Server App: WSGIHandler or StaticFilesHandler / only instance once during server running

BaseHandler (django.core.handlers.base)
    WSGIHandler(base.BaseHandler) (django.core.handlers.wsgi)
        FSFilesHandler(WSGIHandler) (django.test.testcases)
        StaticFilesHandler(StaticFilesHandlerMixin, WSGIHandler) (django.contrib.staticfiles.handlers)
```
