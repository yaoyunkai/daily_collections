"""
查询参数

声明的参数不是路径参数时，路径操作函数会把该参数自动解释为查询参数。


query param 的默认值
            可选参数



created at 2025/2/16
"""

from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
