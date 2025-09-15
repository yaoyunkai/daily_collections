from pyos2 import Scheduler


def foo():
    for i in range(10):
        print('I am foo')
        yield


def bar():
    while True:
        print('I am bar')
        yield


if __name__ == '__main__':
    shced = Scheduler()
    shced.new(foo())
    shced.new(bar())
    shced.mainloop()
