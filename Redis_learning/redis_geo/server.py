"""


created at 2024/9/13
"""
import contextlib
import typing

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from redis_util import geo_search
from redis_util import get_redis_connection

Number = typing.Union[int, float]

G = dict()


@contextlib.asynccontextmanager
async def lifespan(app_: FastAPI):
    try:
        G['redis_db'] = get_redis_connection()
    except Exception as e:
        print(f'connect to redis failed with {e}')

    yield

    if G.get('redis_db'):
        try:
            G['redis_db'].close()
        finally:
            G.pop('redis_db')


app = FastAPI(lifespan=lifespan)


@app.get('/index', response_class=HTMLResponse)
async def index_page():
    with open('index.html', mode='r', encoding='utf8') as f:
        content = f.read()
        return content


@app.get('/nearbySearch', )
async def nearby_search(longitude: Number,
                        latitude: Number,
                        radius: Number, ):
    redis_db = G['redis_db']
    return geo_search(
        'loc', (longitude, latitude), radius, redis_db
    )
