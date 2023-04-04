"""

read的时候会使seek的位置前进

SEEK_SET 文件开头
SEEK_CUR 当前位置
SEEK_END 文件结尾


Created at 2023/4/4
"""
import os


def read_file_in_chunks(file_path, chunk_size=1024):
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk


def reverse_read(filename):
    with open(filename, 'rb') as file:
        file.seek(0, os.SEEK_END)
        pos = file.tell()
        while pos > 0:
            pos -= 1
            file.seek(pos, os.SEEK_SET)
            yield file.read(1)
