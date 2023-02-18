"""
生产者 消费者模型


Created at 2023/2/18
"""
from queue import Queue
from threading import Thread


# 生产者
def produce(q):
    for i in range(1, 11):
        q.put(i)
        print(f'生产产品——{i}')
    q.join()  # 阻塞生产者线程，只有接收到消费者发送来的已经消费了最后一个产品的时候，才解除阻塞


# 消费者
def consumer(q):
    while True:
        tmp = q.get()
        print(f'消费产品——{tmp}')
        q.task_done()  # 向生产者发送消息，告诉生产者我已经消费了一个产品


# 主进程
def main():
    q = Queue()
    pro = Thread(target=produce, args=(q,))
    con = Thread(target=consumer, args=(q,))
    con.setDaemon(True)
    pro.start()
    con.start()


if __name__ == '__main__':
    main()
