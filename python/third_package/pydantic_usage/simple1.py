"""


Create at 2023/3/15 20:08
"""
import pprint
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None

    friends: List[int]


if __name__ == '__main__':
    # print('complied: {}'.format(compiled))  # 验证是否是编译运行的

    external_data = {
        'id': '123',
        'name': 'hhhh"{}',
        'signup_ts': '2019-06-01 12:22',
        'friends': [1, 2, '3'],
    }
    user = User(**external_data)
    print(user.json())
    print(user.dict())
    pprint.pprint(user.schema())

    print(user.__fields_set__)
    print(user.__fields__)
