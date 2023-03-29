"""

task_done:
该方法用于通知队列，一个消费者已经处理完了一个任务。
每当一个消费者完成一个任务时，都应该调用该方法，以便让 join() 方法知道一个任务已经被处理完了。


join:
该方法阻塞主线程，直到队列中的所有任务都被消费者线程处理完毕为止。
也就是说，在主线程中调用该方法会一直阻塞，直到所有任务都被处理完毕，主线程才会继续执行。


Created at 2023/3/28
"""

import queue
import threading
import time


class Producer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(10):
            item = "Item-%s" % i
            self.queue.put(item)
            print("Produced:", item)
            time.sleep(1)


class Consumer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            if item is None:
                break
            print("Consumed:", item)
            self.queue.task_done()


if __name__ == '__main__':
    queue = queue.Queue()

    producer = Producer(queue)
    producer.start()

    consumer = Consumer(queue)
    consumer.start()

    producer.join()
    queue.join()
    consumer.join()
    queue.put(None)
