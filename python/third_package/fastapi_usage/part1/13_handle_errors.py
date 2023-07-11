"""

自定义异常处理

请求中包含无效数据时，FastAPI 内部会触发 RequestValidationError。



Created at 2023/7/10
"""
import os

import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


class UnicornException(Exception):
    def __init__(self, name: str, **kwargs):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


def get_module_name() -> str:
    file_name = os.path.basename(__file__)
    file_name = file_name.replace('.py', '')

    return file_name


if __name__ == '__main__':
    uvicorn.run(f'{get_module_name()}:app', reload=True, port=9000)
