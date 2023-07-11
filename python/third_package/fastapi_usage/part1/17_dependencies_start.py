"""

依赖注入的概念:
    资源（Resource）
    提供方（Provider）
    服务（Service）
    可注入（Injectable）
    组件（Component）

使用async ???

可以做哪些事情:
    关系型数据库
    NoSQL 数据库
    外部支持库
    外部 API
    认证和鉴权系统
    API 使用监控系统
    响应数据注入系统



Created at 2023/7/11
"""
import os
from typing import Union

import uvicorn
from fastapi import Depends
from fastapi import FastAPI

app = FastAPI()


async def common_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/", tags=['demo'], )
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/", tags=['demo'], )
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


def get_module_name() -> str:
    file_name = os.path.basename(__file__)
    file_name = file_name.replace('.py', '')

    return file_name


if __name__ == '__main__':
    uvicorn.run(f'{get_module_name()}:app', reload=True, port=9000)
