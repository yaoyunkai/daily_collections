"""


Created at 2023/3/29
"""
from collections import deque


class ActorScheduler:
    def __init__(self):
        self._actors = {}  # Mapping of names to actors
        self._msg_queue = deque()  # Message queue

    def new_actor(self, name, actor):
        """
        Admit a newly started actor to the scheduler and give it a name
        """
        self._msg_queue.append((actor, None))  # 预激
        self._actors[name] = actor

    def send(self, name, msg):
        """
        Send a message to a named actor
        """
        actor = self._actors.get(name)
        if actor:
            self._msg_queue.append((actor, msg))

    def run(self):
        """
        Run as long as there are pending messages.
        """
        # 只有在queue不为空的时候才返回True
        while self._msg_queue:
            actor, msg = self._msg_queue.popleft()
            try:
                actor.send(msg)
            except StopIteration:
                pass


def printer():
    print('call printer ...')
    while True:
        msg = yield
        print('Got:', msg)


def counter(scheduler):
    print('call counter ...')

    while True:
        # Receive the current count
        n = yield
        if n == 0:
            break
        # Send to the printer task
        scheduler.send('printer', n)
        # Send the next count to the counter task (recursive)
        scheduler.send('counter', n - 1)


if __name__ == '__main__':
    sched = ActorScheduler()
    # Create the initial actors
    sched.new_actor('printer', printer())
    sched.new_actor('counter', counter(sched))

    # Send an initial message to the counter to initiate
    sched.send('counter', 30)
    sched.run()

    # g = printer()
    # g.send(None)  # 预激  next(g)
    # g.send(345)
    # g.send(567)
