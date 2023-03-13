"""


Created at 2023/3/13
"""
import time

from retask import Queue

queue = Queue('example')
queue.connect()


if __name__ == '__main__':
    queue = Queue('example')
    queue.connect()

    try:
        while True:
            if queue.length == 0:
                time.sleep(1)
                # print('---- time sleep 1 ----')
            else:
                task = queue.dequeue()
                print(task.data)
    except KeyboardInterrupt:
        raise
