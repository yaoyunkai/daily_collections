"""


created at 2024/9/13
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/index', response_class=HTMLResponse)
async def index_page():
    with open('index.html', mode='r', encoding='utf8') as f:
        content = f.read()
        return content
