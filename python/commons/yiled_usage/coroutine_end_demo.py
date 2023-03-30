"""

cor.throw

cor.close


Created at 2023/3/30
"""


class DemoException(Exception):
    pass


def demo_finally():
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing...')
            else:
                print('-> coroutine received: {!r}'.format(x))

    finally:
        print('-> coroutine ending')


if __name__ == '__main__':
    cor = demo_finally()
    cor.send(None)

    cor.send(123)
    cor.send(234)
    cor.send(345)

    cor.throw(DemoException)
    cor.close()
