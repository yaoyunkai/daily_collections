"""
__set_name__
    owner: 被包装的类对象
    name : 参数名


Created at 2023/3/27
"""

import logging

logging.basicConfig(level=logging.INFO)


class LoggedAccess:

    def __set_name__(self, owner, name):
        print(owner, name)
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = getattr(obj, self.private_name)
        logging.info('Accessing %r giving %r', self.public_name, value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', self.public_name, value)
        setattr(obj, self.private_name, value)


class Person:
    name = LoggedAccess()  # First descriptor instance
    age = LoggedAccess()  # Second descriptor instance

    def __init__(self, name, age):
        self.name = name  # Calls the first descriptor
        self.age = age  # Calls the second descriptor

    def birthday(self):
        self.age += 1


if __name__ == '__main__':
    ret = vars(Person)['name']
    print(ret)

    print(Person.name)
