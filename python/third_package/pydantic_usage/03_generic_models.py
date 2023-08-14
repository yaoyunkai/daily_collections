"""


Created at 2023/8/14
"""

from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ValidationError
from pydantic import validator
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class Error(BaseModel):
    code: int
    message: str


class DataModel(BaseModel):
    numbers: List[int]
    people: List[str]


# DataT 相当于形参
class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]
    error: Optional[Error]

    @validator('error', always=True)
    def check_consistency(cls, v, values):
        if v is not None and values['data'] is not None:
            raise ValueError('must not provide both data and error')
        if v is None and values.get('data') is None:
            raise ValueError('must provide data or error')
        return v


data = DataModel(numbers=[1, 2, 3], people=[])
error = Error(code=404, message='Not found')

# int 相当于实参
print(Response[int](data=1).json())
# > data=1 error=None
print(Response[str](data='value'))
# > data='value' error=None
print(Response[str](data='value').dict())
# > {'data': 'value', 'error': None}
print(Response[DataModel](data=data).dict())
"""
{
    'data': {'numbers': [1, 2, 3], 'people': []},
    'error': None,
}
"""
print(Response[DataModel](error=error).dict())
"""
{
    'data': None,
    'error': {'code': 404, 'message': 'Not found'},
}
"""
try:
    Response[int](data='value')
except ValidationError as e:
    print(e)
    """
    2 validation errors for Response[int]
    data
      value is not a valid integer (type=type_error.integer)
    error
      must provide data or error (type=value_error)
    """
