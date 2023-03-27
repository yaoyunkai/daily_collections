"""


Created at 2023/3/27
"""

import logging

logging.basicConfig(level=logging.INFO)


class LoggedAgeAccess:

    def __get__(self, obj, objtype=None):
        value = obj._age
        logging.info('Accessing %r giving %r', 'age', value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', 'age', value)
        obj._age = value


class Person:
    age = LoggedAgeAccess()  # Descriptor instance

    def __init__(self, name, age):
        self.name = name  # Regular instance attribute
        self.age = age  # Calls __set__()

    def birthday(self):
        self.age += 1  # Calls both __get__() and __set__()


if __name__ == '__main__':
    mary = Person('Mary M', 30)  # The initial age update is logged
    dave = Person('David D', 40)

    print(vars(mary))  # The actual data is in a private attribute
    print(vars(dave))

    print(mary.age)  # Access the data and log the lookup

    mary.birthday()  # Updates are logged as well

    print(dave.name)  # Regular attribute lookup isn't logged

    print(dave.age)  # Only the managed attribute is logged
