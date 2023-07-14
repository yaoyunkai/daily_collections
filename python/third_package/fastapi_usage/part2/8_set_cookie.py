"""

Set Cookie
Response
Request


Created at 2023/7/14
"""

from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI()


@app.post("/cookie-and-object/")
def create_cookie(response: Response, request: Request):
    client_host = request.client.host
    print(client_host)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}


@app.post("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.headers["X-Cat-Dog"] = "alone in the world"
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response
