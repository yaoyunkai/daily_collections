"""

Queue:
    names: 获取所有队列

    length: llen 获取队列长度

    connect: connect to redis

    wait(wait_time=0):
        wait_time = 0 表示一直block 直到获取到数据
        data = brpop(self._name)
        return task(data[1])

    dequeue:
        if llen == 0 return None
        data = rpop(self._name) : 立即的 return null or element
        return Task(data)

    enqueue(Task):
        job = Job(self.conn)
        task.urn = job.urn
        lpush (self._name, task)
        return job

    send(task, result, expire=60):
        lpush(task.urn, json.dumps(result))
        expire(task.urn, expire)

    find



Job:
    __init__
        rdb = Conn
        urn = uuid
        __result = None


    result():
        if _result:
            return _result
        data = self.rdb.rpop(self.urn)
        if data:
            self.rdb.delete(self.urn)
            data = json.loads(data)
            self.__result = data
            return data

    wait(wait_time):
        if self.__result:
            return True
        data = self.rdb.brpop(self.urn, wait_time)  # brpop的返回值是 arr, element的形式
        if data:
            self.rdb.delete(self.urn)
            data = json.loads(data[1])
            self.__result = data
            return True
        else:
            return False

Task
    __init__(raw=False)
        _data
        urn

    func: data:
        json.loads(_data)



Created at 2023/3/13
"""

from retask import Queue
from retask import Task

if __name__ == '__main__':
    queue = Queue('example')
    queue.connect()

    # info1 = {'user': 'kushal', 'url': 'http://kushaldas.in'}
    # info2 = {'user': 'fedora planet', 'url': 'http://planet.fedoraproject.org'}
    # task1 = Task(info1)
    # task2 = Task(info2)
    # queue.enqueue(task1)
    # queue.enqueue(task2)

    while True:
        out = input('Please enter task: ')
        if out == 'END':
            break

        task = Task(out)
        queue.enqueue(task)
