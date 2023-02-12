# retask

## 目录

-   [同步方式](#同步方式)
-   [异步方式](#异步方式)
-   [API](#API)
    -   [Queue](#Queue)
    -   [Job](#Job)
    -   [Task](#Task)

```纯文本
task 入队列的key是: 'retaskqueue-' + name

consumer从 'retaskqueue-' + name 获取任务 (dequeue / wait)

consumer 把结果发送给task, key 是 urn:uuid:84577c90-8a0c-4de5-915d-4bc6c9fcfb79

producer 从key里面: urn:uuid:84577c90-8a0c-4de5-915d-4bc6c9fcfb79 获取结果

------------------------------------------------

在没有使用 Job类的情况下, 只使用了一种redis Key: 'retaskqueue-' + name

job-version: xxxxxx

{
    job_name:
    job_client_version:
    job_params:

}

```

## 同步方式

producer:&#x20;

```python
from retask import Queue
from retask import Task

queue = Queue('example')

info1 = {'user': 'kushal', 'url': 'https://kushaldas.in'}
info2 = {'user': 'fedora planet', 'url': 'https://planet.fedoraproject.org'}
task1 = Task(info1)
task2 = Task(info2)

queue.connect()
queue.enqueue(task1)
queue.enqueue(task2)
```

consumer:

```python
from retask import Queue

queue = Queue('example')
queue.connect()

while queue.length != 0:
    task = queue.dequeue()
    if task:
        print(task.data)

```

## 异步方式

producer:

```python
import time

from retask import Queue
from retask import Task

queue = Queue('example')
info1 = {'user': 'Fedora planet', 'url': 'http://planet.fedoraproject.org'}
task1 = Task(info1)
queue.connect()
job = queue.enqueue(task1)
print(job.result)
time.sleep(30)
print(job.result)

```

consumer:

```python
import time

from retask import Queue

queue = Queue('example')
queue.connect()


task = queue.wait()
print(task.data)
time.sleep(15)
queue.send(task, "We received your information dear %s" % task.data['user'])

```

## API

### Queue

Returns the `Queue` object with the given name. If the user passes optional config dictionary with details for Redis server, it will connect to that instance. By default it connects to the localhost.

`connect()`
Creates the connection with the redis server. Return `True` if the connection works, else returns `False`. It does not take any arguments.

dequeue

enqueue

wait

### Job

result

wait

### Task

Returns a new Task object, the information for the task is passed through argument *data*.

Task object 包装了data属性和urn属性。
