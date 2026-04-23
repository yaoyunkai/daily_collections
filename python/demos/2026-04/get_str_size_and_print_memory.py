"""
get_str_size.py

获取str 底层的实际大小

1,2,4 字节。

根据unicode的码位来计算使用1 2 4个字节来表示一个字符.



created at 2026-04-23
"""

import ctypes
import sys

# s1 = "abc"
# s2 = "abc一二三"

# print(f"s1 size: {sys.getsizeof(s1)} bytes")
# print(f"s2 size: {sys.getsizeof(s2)} bytes")


def dump_memory(obj):
    """
    获取并打印 Python 对象在内存中的真实字节表示
    """
    # 1. 获取对象的真实内存地址
    addr = id(obj)
    # 2. 获取对象在内存中占用的总字节数
    size = sys.getsizeof(obj)

    # 3. 使用 ctypes 创建一个指向该地址的 C 语言字节数组指针，并读取数据
    raw_bytes = (ctypes.c_ubyte * size).from_address(addr)

    print(f"=== Object: {repr(obj)} ===")
    print(f"Address: {hex(addr)} | Size: {size} bytes")
    print("-" * 70)

    # 4. 格式化输出 (类似 Hex Editor)
    for i in range(0, size, 16):
        chunk = raw_bytes[i : i + 16]
        # 转换为十六进制字符串
        hex_str = " ".join(f"{b:02x}" for b in chunk)
        # 尝试打印可读的 ASCII 字符，不可读的用 '.' 代替
        ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)

        # 打印：内存偏移量 | 十六进制字节 | ASCII 预览
        print(f"+{i:02x} ( {i:02d} )  {hex_str:<47}  |{ascii_str}|")
    print("=" * 70 + "\n")


def dump_memory_with_string_at(obj):
    """
    使用 ctypes.string_at 获取并打印 Python 对象在内存中的真实字节
    """
    addr = id(obj)
    size = sys.getsizeof(obj)

    # 核心改动：直接读取指定地址和长度的内存，返回一个标准的 bytes 对象
    raw_bytes = ctypes.string_at(addr, size)

    print(f"=== Object: {repr(obj)} ===")
    print(f"Address: {hex(addr)} | Size: {size} bytes")
    print("-" * 70)

    # 遍历 bytes 对象进行 Hex 格式化输出
    for i in range(0, size, 16):
        # 切片操作，每次取 16 个字节
        chunk = raw_bytes[i : i + 16]

        # 在 Python 3 中，迭代 bytes 对象得到的是 int (0-255)
        hex_str = " ".join(f"{b:02x}" for b in chunk)
        ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)

        print(f"+{i:02x} ( {i:02d} )  {hex_str:<47}  |{ascii_str}|")
    print("=" * 70 + "\n")


# 测试我们之前讨论的两个字符串
if __name__ == "__main__":
    s1 = "abc"
    s2 = "abc一二三"

    # dump_memory(s1)
    # dump_memory(s2)
    dump_memory_with_string_at(s1)
    dump_memory_with_string_at(s2)
