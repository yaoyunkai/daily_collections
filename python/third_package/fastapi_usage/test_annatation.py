"""
测试注解


Created at 2023/7/10
"""
import inspect
from typing import List

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str


def test_func(param1=List[Item]):
    pass


if __name__ == '__main__':
    # 获取 test_func 的签名信息
    sig = inspect.signature(test_func)

    # 获取参数 param1 的注解
    # objprint.op(sig.parameters['param1'])
    print(sig.parameters['param1'])
