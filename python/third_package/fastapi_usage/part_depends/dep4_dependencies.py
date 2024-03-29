"""

dependencies声明的依赖项 不会返回值

同时也可以声明全局依赖项:

    app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

Created at 2023/8/15
"""

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Header

app = FastAPI()


async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
