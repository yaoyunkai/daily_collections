"""
application/x-www-form-urlencoded
multipart/form-data



Created at 2023/7/10
"""
import os

import uvicorn
from fastapi import FastAPI
from fastapi import Form

app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


def get_module_name() -> str:
    file_name = os.path.basename(__file__)
    file_name = file_name.replace('.py', '')

    return file_name


if __name__ == '__main__':
    uvicorn.run(f'{get_module_name()}:app', reload=True, port=9000)
