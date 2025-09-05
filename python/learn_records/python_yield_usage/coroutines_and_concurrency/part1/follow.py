import time
from io import SEEK_END


def follow(fileobj):
    fileobj.seek(0, SEEK_END)
    while True:
        line = fileobj.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == '__main__':
    fp = open('demo.txt', mode='r', encoding='utf8')
    for line in follow(fp):
        print(line)
