"""

如果在路径中也声明了该参数，它将被用作路径参数。
如果参数属于单一类型（比如 int、float、str、bool 等）它将被解释为查询参数。
如果参数的类型被声明为一个 Pydantic 模型，它将被解释为请求体。

Created at 2023/8/15
"""
from typing import Union

from fastapi import Depends
from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:

    # 没有return depends是如何知道返回了什么
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
# async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response


@app.post("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items, 'method': 'post'})
    return response


if __name__ == '__main__':
    run(app, )
