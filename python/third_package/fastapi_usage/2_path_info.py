"""
Created at 2023/7/6


"""

from enum import Enum
from typing import Union

from fastapi import FastAPI


class ModelName(str, Enum):
    """
    如果你有一个接收路径参数的路径操作，但你希望预先设定可能的有效参数值，则可以使用标准的 Python Enum 类型。
    
    """
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    """
    在这里 q是可选参数
    
    """
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
