"""

FastAPI 不会为同一个请求多次调用同一个依赖项，而是把依赖项的返回值进行「缓存」，
并把它传递给同一请求中所有需要使用该返回值的「依赖项」。

Created at 2023/8/15
"""

from typing import Union

from fastapi import Cookie
from fastapi import Depends
from fastapi import FastAPI

app = FastAPI()


def query_extractor(q: Union[str, None] = None):
    return q


def query_or_cookie_extractor(
        q: str = Depends(query_extractor),
        last_query: Union[str, None] = Cookie(default=None),
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
