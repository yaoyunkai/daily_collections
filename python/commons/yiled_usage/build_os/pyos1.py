"""
file: pyos1.py
Created by Libyao at 2023/4/5


"""


class Task(object):
    __task_id = 0

    def __init__(self, target):
        Task.__task_id += 1
        self.tid = Task.__task_id
        self.target = target
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)


if __name__ == '__main__':
    def foo():
        print("Part 1")
        yield
        print("Part 2")
        yield


    t1 = Task(foo())
    print("Running foo()")
    t1.run()
    print("Resuming foo()")
    t1.run()
