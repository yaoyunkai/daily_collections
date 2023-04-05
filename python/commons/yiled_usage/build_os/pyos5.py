"""
file: pyos5.py
Created by Libyao at 2023/4/5

More System Call:
    new task
    kill task



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
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue

            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)


class SystemCall:
    task = None
    sched = None

    def handle(self):
        pass


class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)


class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid  # 把new task的id返回给开启这个newtask的task
        self.sched.schedule(self.task)


class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        task = self.sched.taskmap.get(self.tid, None)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched.schedule(self.task)


if __name__ == '__main__':

    def foo():
        tid = yield GetTid()
        while True:
            print("I'm foo", tid)
            yield


    def main():
        child = yield NewTask(foo())  # Launch new task
        for i in range(5):
            yield
        result = yield KillTask(child)  # Kill the task
        print("main done, child killed result:", result)


    sched = Scheduler()
    sched.new(main())
    sched.mainloop()
