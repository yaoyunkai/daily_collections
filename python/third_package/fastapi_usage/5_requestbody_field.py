"""
Created at 2023/7/6

Request Body: Field

实际上，Query、Path 和其他你将在之后看到的类，
创建的是由一个共同的 Params 类派生的子类的对象，该共同类本身又是 Pydantic 的 FieldInfo 类的子类。


"""
from typing import Union

from fastapi import Body
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
