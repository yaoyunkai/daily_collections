"""
file: task_crash.py
Created by Libyao at 2023/4/5


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

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            result = task.run()
            self.schedule(task)


if __name__ == '__main__':

    # Two tasks
    def foo():
        for i in range(10):
            print("I'm foo")
            yield


    def bar():
        while True:
            print("I'm bar")
            yield

            # Run them


    sched = Scheduler()
    sched.new(foo())
    sched.new(bar())
    sched.mainloop()
