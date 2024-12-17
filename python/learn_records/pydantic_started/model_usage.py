"""

dict: ???? 已弃用

model_dump -> dict response
model_dump_json

model_construct

model_validate            from dict or json data
model_validate_json
model_validate_strings


model_fields
model_computed_fields

model_fields_set           初始化传入的字段。

---------------------------------------------------------

from_orm



created at 2024/12/17
"""

from pydantic import BaseModel


# class User(BaseModel):
#     id: int
#     name: str = 'Jane Doe'
#     num: Optional[int] = 0

class User(BaseModel):
    id: int
    name: str
    signup_ts: str = None


if __name__ == '__main__':
    for k in vars(User):
        print(k)

    # 正确的示例：使用字典作为输入
    data = {'id': 123, 'name': 'John Doe', 'signup_ts': '2019-06-01 12:22'}
    user = User.model_validate(data)
    print(user)

    user2 = User.model_construct(id='abc', name=1234,)
    print(user2)
    print(user2.model_fields_set)
    # user3 = User.model_validate(user2.model_dump())

    # print(user2.model_extra)

