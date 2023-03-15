"""


Create at 2023/3/15 20:08
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ValidationError, compiled


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


if __name__ == '__main__':
    external_data = {
        'id': '123',
        'signup_ts': '2019-06-01 12:22',
        'friends': [1, 2, '3'],
    }
    user = User(**external_data)
    print('complied: {}'.format(compiled))  # 验证是否是编译运行的
    print(user.json())

    # print(user.id)
    # print(user.signup_ts)
    # print(user.friends)
    # print(user.dict())

    try:
        User(id=124, name='Tom', friends=[1, 2, 'xx'])
    except ValidationError as e:
        print(e.json())
