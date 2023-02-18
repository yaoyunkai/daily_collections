"""


Created at 2023/2/18
"""
import threading

# Threading.local对象
localManager = threading.local()
lock = threading.RLock()


class MyThead(threading.Thread):
    def __init__(self, thread_name, name):
        super(MyThead, self).__init__(name=thread_name)
        self.__name = name

    def run(self):
        # global localManager
        localManager.ThreadName = self.name
        localManager.Name = self.__name
        MyThead.ThreadPoc()

    # 线程处理函数
    @staticmethod
    def ThreadPoc():
        lock.acquire()
        try:
            print('Thread={id}'.format(id=localManager.ThreadName))
            print('Name={name}'.format(name=localManager.Name))
        finally:
            lock.release()


if __name__ == '__main__':
    bb = {'Name': 'bb'}
    aa = {'Name': 'aa'}
    xx = (aa, bb)
    threads = [MyThead(thread_name='id_{0}'.format(i), name=xx[i]['Name']) for i in range(len(xx))]
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()
