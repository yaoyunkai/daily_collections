"""
路径参数

路径参数 -- 对应方法参数

方法定义的顺序。


"""
from enum import Enum

from fastapi import FastAPI

app = FastAPI()


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


app2 = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app2.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # 与Enum 实例比较
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


app3 = FastAPI()


@app3.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    假设路径操作的路径为 /files/{file_path}。
    但需要 file_path 中也包含路径，比如，home/johndoe/myfile.txt。
    此时，该文件的 URL 是这样的：/files/home/johndoe/myfile.txt。


    """
    return {"file_path": file_path}
