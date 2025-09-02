"""
file: pyos3.py
Created by Libyao at 2023/4/5

Handle Task exit


"""
from queue import Queue


class Task(object):
    __task_id = 0

    def __init__(self, target):
        Task.__task_id += 1
        self.tid = Task.__task_id
        self.target = target
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)


class Scheduler(object):
    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}

    def new(self, target):
        """
        只有当new的时候 taskmap才会被改变

        :param target:
        :return:
        """
        new_task = Task(target)
        self.taskmap[new_task.tid] = new_task
        self.schedule(new_task)
        return new_task.tid

    def exit(self, task):
        print("Task %d terminated", task.tid)
        del self.taskmap[task.tid]

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)


if __name__ == '__main__':

    def foo():
        for i in range(10):
            print("I'm foo")
            yield


    def bar():
        for i in range(5):
            print("I'm bar")
            yield


    sched = Scheduler()
    sched.new(foo())
    sched.new(bar())
    sched.mainloop()
