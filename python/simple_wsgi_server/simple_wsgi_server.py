"""
protocol: https://peps.python.org/pep-3333/

继承层次:

BaseServer (socketserver stub)
    TCPServer(BaseServer) (socketserver stub)
        HTTPServer(socketserver.TCPServer) (http.server stub)
            WSGIServer(HTTPServer) (wsgiref.simple_server)

Django Dev Simple Server:

Server class: WSGIServer(simple_server.WSGIServer)

RequestHandlerClass: WSGIRequestHandler(simple_server.WSGIRequestHandler)
    request handler 委派 ServerHandler(simple_server.ServerHandler) 处理请求

Server App: WSGIHandler or StaticFilesHandler / only instance once during server running

BaseHandler (django.core.handlers.base)
    WSGIHandler(base.BaseHandler) (django.core.handlers.wsgi)
        FSFilesHandler(WSGIHandler) (django.test.testcases)
        StaticFilesHandler(StaticFilesHandlerMixin, WSGIHandler) (django.contrib.staticfiles.handlers)


Created at 2023/3/1
"""

from wsgiref.simple_server import WSGIServer, WSGIRequestHandler


def demo_app(environ, start_response):
    from io import StringIO
    stdout = StringIO()
    print("Hello world!", file=stdout)
    print(file=stdout)
    h = sorted(environ.items())
    for k, v in h:
        print(k, '=', repr(v), file=stdout)
    start_response("200 OK", [('Content-Type', 'text/plain; charset=utf-8')])
    return [stdout.getvalue().encode("utf-8")]


def make_server(
        host, port, app, server_class=WSGIServer, handler_class=WSGIRequestHandler
):
    """Create a new WSGI server listening on `host` and `port` for `app`"""
    server = server_class((host, port), handler_class)
    server.set_app(app)
    return server


if __name__ == '__main__':
    make_server('localhost', 8080, demo_app, ).serve_forever()
