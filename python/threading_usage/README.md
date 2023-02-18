# Threading usage

`threading.active_count()`  返回当前存活的 Thread 对象的数量。

`threading.current_thread()` 返回当前对应调用者的控制线程的 Thread 对象。

`threading.excepthook(args, /)` 处理由 Thread.run() 引发的未捕获异常。

`threading.get_ident()` 返回当前线程的 “线程标识符”。

`threading.enumerate()` 返回当前所有存活的 Thread 对象的列表。

`threading.main_thread()` 返回主 Thread 对象。

## 线程本地数据

```python
mydata = threading.local()
mydata.x = 1
```

## 线程对象 Thread

Thread 类代表在独立控制线程运行的活动。有两种方式指定活动：传递一个可调用对象给构造函数或者在子类重载 run() 方法。其它方法不应该在子类被（除了构造函数）重载。换句话说，只能 重载这个类的 `__init__()` 和 `run()` 方法。

当线程对象一旦被创建，其活动必须通过调用线程的 `start()` 方法开始。

 `is_alive()` 检查线程是否还存活。

`join()` 这会阻塞调用该方法的线程，直到被调用 `join()` 方法的线程终结。

` daemon` 后台线程，这个标识的意义是，当剩下的线程都是守护线程时，整个 Python 程序将会退出。

守护线程在程序关闭时会突然关闭。他们的资源（例如已经打开的文档，数据库事务等等）可能没有被正确释放。如果你想你的线程正常停止，设置他们成为非守护模式并且使用合适的信号机制。

## 锁对象

原始锁是一个在锁定时不属于特定线程的同步基元组件。在Python中，它是能用的最低级的同步基元组件，由 _thread 扩展模块直接实现。

原始锁处于 "锁定" 或者 "非锁定" 两种状态之一。它被创建时为非锁定状态。

当状态为非锁定时，`acquire()` 将状态改为 锁定 并立即返回。当状态是锁定时， `acquire()` 将阻塞至其他线程调用 `release()` 将其改为非锁定状态，然后 `acquire()` 调用重置其为锁定状态并返回。 `release()` 只在锁定状态下调用； 它将状态改为非锁定并立即返回。如果尝试释放一个非锁定的锁，则会引发 `RuntimeError`  异常。

当多个线程在 acquire() 等待状态转变为未锁定被阻塞，然后 release() 重置状态为未锁定时，只有一个线程能继续执行；至于哪个等待线程继续执行没有定义，并且会根据实现而不同。

## RLock

重入锁是一个可以被同一个线程多次获取的同步基元组件。在内部，它在基元锁的锁定/非锁定状态上附加了 "所属线程" 和 "递归等级" 的概念。在锁定状态下，某些线程拥有锁 ； 在非锁定状态下， 没有线程拥有它。

若要锁定锁，线程调用其 `acquire()` 方法；一旦线程拥有了锁，方法将返回。若要解锁，线程调用 `release()` 方法。 `acquire()/release()` 对可以嵌套；只有最终 `release()` (最外面一对的 `release()` ) 将锁解开，才能让其他线程继续处理 `acquire()` 阻塞。

默认的Lock不识别锁当前持有的线程。

[When and how to use Python's RLock - Stack Overflow](https://stackoverflow.com/questions/16567958/when-and-how-to-use-pythons-rlock)

