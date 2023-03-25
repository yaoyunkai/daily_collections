"""


Created at 2023/3/13
"""

from retask import Queue
from retask import Task

if __name__ == '__main__':
    queue = Queue('example')
    queue.connect()

    while True:
        out = input('Please enter task: {conn,action} :')
        if out == 'END':
            break
        conn, action = out.strip().split(',')
        task = Task({'conn': conn, 'action': action})
        job = queue.enqueue(task)
        job.wait()
        print(job.result)
