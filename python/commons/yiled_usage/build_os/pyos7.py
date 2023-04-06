"""

add IO loop support

select timeout:
1. 不存在 None : 永远不会超时
2. 0          : 没有信号就返回



Created at 2023/4/6
"""
from queue import Queue

import select


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

        self.exit_waiting = {}

        # I/O waiting
        self.read_waiting = {}
        self.write_waiting = {}

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

        # Notify other tasks waiting for exit
        for task_obj in self.exit_waiting.pop(task.tid, []):
            # 只有这里schedule之后, 等待的task才会有机会往下执行
            self.schedule(task_obj)

    def waitforexit(self, task, wait_tid):
        """

        :param task: 等待的task
        :param wait_tid: 被等待的task
        :return:
        """
        if wait_tid in self.taskmap:
            self.exit_waiting.setdefault(wait_tid, []).append(task)
            return True
        else:
            return False

    def waitforread(self, task, fd):
        self.read_waiting[fd] = task

    def waitforwrite(self, task, fd):
        self.write_waiting[fd] = task

    def iopoll(self, timeout):
        if self.read_waiting or self.write_waiting:
            r, w, e = select.select(self.read_waiting, self.write_waiting, [], timeout)

            for fd in r:
                self.schedule(self.read_waiting.pop(fd))
            for fd in w:
                self.schedule(self.write_waiting.pop(fd))

    def iotask(self):
        while True:
            if self.ready.empty():
                self.iopoll(None)
            else:
                self.iopoll(0)
            yield

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):
        self.new(self.iotask())
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


class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        result = self.sched.waitforexit(self.task, self.tid)
        self.task.sendval = result
        if not result:
            self.sched.schedule(self.task)


class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforread(self.task, fd)


class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforwrite(self.task, fd)


if __name__ == '__main__':

    def foo():
        for i in range(5):
            print("I'm foo")
            yield


    def main():
        child = yield NewTask(foo())
        print("Waiting for child")
        rr = yield WaitTask(child)
        print('result:', rr)
        print("Child done")


    sched = Scheduler()
    sched.new(main())
    sched.mainloop()
