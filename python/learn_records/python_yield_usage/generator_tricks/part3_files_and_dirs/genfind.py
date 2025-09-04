"""

Path.rglob()


"""

from pathlib import Path


def gen_find(filepat, top):
    yield from Path(top).rglob(filepat)


if __name__ == '__main__':
    lognames = gen_find("access-log*", "www")
    for name in lognames:
        print(name)
