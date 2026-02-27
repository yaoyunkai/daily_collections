import sys
import struct


def get_cpu_endian():
    if sys.byteorder == 'little':
        print("当前系统是：小端模式 (Little-Endian)")
    else:
        print("当前系统是：大端模式 (Big-Endian)")

    print(f"系统原生字节序: {sys.byteorder}")


def check_endian():
    # 'h' 代表 short (2字节整数)
    # 将数字 1 打包成二进制数据
    packed_data = struct.pack('h', 1)

    print(f"数字 1 打包后的字节数据: {packed_data}")

    if packed_data == b'\x01\x00':
        return "小端模式 (Little-Endian)"
    elif packed_data == b'\x00\x01':
        return "大端模式 (Big-Endian)"
    else:
        return "未知模式"


print(check_endian())
