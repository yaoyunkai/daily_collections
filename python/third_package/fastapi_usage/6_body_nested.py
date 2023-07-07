"""


Created at 2023/7/7
"""
from typing import Dict
from typing import List
from typing import Set
from typing import Union

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image], None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[str, float]):
    return weights


if __name__ == '__main__':
    uvicorn.run(app)
