"""


Created at 2023/3/13
"""

import time

from retask import Queue

if __name__ == '__main__':
    queue = Queue('example')
    queue.connect()
    try:
        while True:
            task = queue.wait()
            print(task.data)
            time.sleep(30)
            queue.send(task, "We received your information conn: {}, action is {}".format(
                task.data['conn'], task.data['action']))
    except KeyboardInterrupt:
        print('finish ....')
