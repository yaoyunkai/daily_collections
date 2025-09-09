class Task:
    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)


if __name__ == '__main__':
    def foo():
        print('Part 1')
        yield
        print('Part 2')
        yield


    t1 = Task(foo())
    print("Running foo()")
    t1.run()
    print("Resuming foo()")
    t1.run()

    # If you call t1.run() one more time, you get StopIteration.
    # Uncomment the next statement to see that.

    # t1.run()
