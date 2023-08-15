"""


Created at 2023/8/15
"""

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request

from uvicorn import run

app = FastAPI()


def get_query_param(request: Request):
    return request.query_params.get("cc")


def get_header_value(request: Request):
    return request.headers.get("dd")


@app.get("/items/", tags=['tests'])
async def read_item(param_value: str = Depends(get_query_param), header_value: str = Depends(get_header_value)):
    return {"param_value": param_value, "header_value": header_value}


def get_item_id(item_id: str, param1: str):
    print(item_id)
    print(param1)
    return {'item': 'simple item'}


@app.get('/item/{item_id}/', tags=['tests'])
async def test_pathinfo_with_depend(item_obj: dict = Depends(get_item_id)):
    return item_obj


if __name__ == '__main__':
    run(app, )
