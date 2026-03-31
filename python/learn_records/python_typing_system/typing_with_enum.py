"""
Enum 的使用

IntEnum IntFlag
不建议使用 IntEnum

"""

from enum import Enum, Flag, auto


class Permission(Enum):
    READ = 0b_0001
    WRITE = 0b_0010
    EXECUTE = 0b_0100


class PermFlag(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


def usage_of_enum():
    print(Permission.WRITE)
    print(type(Permission.WRITE))

    for option_number, perm in enumerate(Permission, start=1):
        print(f"Option level {option_number}, {perm}")

    # Enum 类型和 int 不能比较
    print(Permission.READ == 1)
    print(Permission.READ.value)

    for perm in PermFlag:
        print(f"{perm.name}: {perm.value}")


if __name__ == "__main__":
    usage_of_enum()
