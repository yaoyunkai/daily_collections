"""
ASGI Application

app(scope receive send)

<uvicorn.protocols.http.httptools_impl.RequestResponseCycle>  run_asgi

Created at 2023/9/11
"""

demo_scope = {
    'type': 'http',
    'asgi': {'version': '3.0', 'spec_version': '2.3'},
    'http_version': '1.1',
    'server': ('127.0.0.1', 8000),
    'client': ('127.0.0.1', 5385),
    'scheme': 'http',
    'root_path': '',
    'headers': [(b'host', b'127.0.0.1:8000'),
                (b'connection', b'keep-alive'),
                (b'cache-control', b'max-age=0'),
                (b'sec-ch-ua', b'"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"'),
                (b'sec-ch-ua-mobile', b'?0'),
                (b'sec-ch-ua-platform', b'"Windows"'),
                (b'upgrade-insecure-requests', b'1'),
                (b'user-agent', b''),
                (b'accept', b'text/html,application/xhtml+xml'),
                (b'sec-fetch-site', b'none'),
                (b'sec-fetch-mode', b'navigate'),
                (b'sec-fetch-user', b'?1'),
                (b'sec-fetch-dest', b'document'),
                (b'accept-encoding', b'gzip, deflate, br'),
                (b'accept-language', b'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'),
                (b'cookie', b'csrftoken=NG9YRRdxnJHLFxOMzLEuegXoqU1flCic; sessionid=7bdnnsl505eqafpecnfnb8mxlptt2vty')],
    'state': {},
    'method': 'GET',
    'path': '/',
    'raw_path': b'/',
    'query_string': b''
}
