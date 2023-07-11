"""
Created at 2023/7/6

Query 的第一个参数同样也是用于定义默认值。

可以用 alias 参数声明一个别名，该别名将用于在 URL 中查找查询参数值


"""

from typing import Union

import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
        q: Union[str, None] = Query(
            default=None,
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


if __name__ == '__main__':
    uvicorn.run(app)
