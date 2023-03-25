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

## Condition

Condition被称为条件变量，除了提供与Lock类似的acquire和release方法外，还提供了wait和notify方法。

### Condition的处理流程

- 首先acquire一个条件变量，然后判断一些条件。
- 如果条件不满足则wait；
- 如果条件满足，进行一些处理改变条件后，通过notify方法通知其他线程，其他处于wait状态的线程接到通知后会重新判断条件。
- 不断的重复这一过程，从而解决复杂的同步问题。

### Condition原理

可以认为Condition对象维护了一个锁（Lock/RLock)和一个waiting池。线程通过acquire获得Condition对象，当调用wait方法时，线程会释放Condition内部的锁并进入blocked状态，同时在waiting池中记录这个线程。当调用notify方法时，Condition对象会从waiting池中挑选一个线程，通知其调用acquire方法尝试取到锁。

除了notify方法外，Condition对象还提供了notifyAll方法，可以通知waiting池中的所有线程尝试acquire内部锁。由于上述机制，**处于waiting状态的线程只能通过notify方法唤醒，所以notifyAll的作用在于防止有的线程永远处于沉默状态。**

## Event

很多时候，线程之间会有互相通信的需要。常见的情形是次要线程为主要线程执行特定的任务，在执行过程中需要不断报告执行的进度情况。

`threading.Event`可以使一个线程等待其他线程的通知。其内置了一个标志，初始值为False。线程通过wait()方法进入等待状态，直到另一个线程调用set()方法将内置标志设置为True时，Event通知所有等待状态的线程恢复运行；调用clear()时重置为 False。还可以通过isSet()方法查询Envent对象内置状态的当前值。

Event其实就是一个简化版的 Condition。Event没有锁，无法使线程进入同步阻塞状态。

- `isSet()`: 当内置标志为True时返回True。
- `set()`: 将标志设为True，并通知所有处于等待阻塞状态的线程恢复运行状态。
- `clear()`: 将标志设为False。
- `wait([timeout])`: 如果标志为True将立即返回，否则阻塞线程至等待阻塞状态，等待其他线程调用set()。

## Timer

Timer（定时器）是Thread的派生类，用于在指定时间后调用一个方法。Timer从Thread派生，没有增加实例方法。

- interval: 指定的时间
- function: 要执行的方法
- args/kwargs: 方法的参数

Timers通过调用它们的start()方法作为线程启动。

timer可以通过调用cancel()方法（在它的动作开始之前）停止。

timer在执行它的动作之前等待的时间间隔可能与用户指定的时间间隔不完全相同。

## Threading Local

一般我们对多线程中的全局变量都会加锁处理，这种变量是共享变量，每个线程都可以读写变量，为了保持同步我们会做枷锁处理。

但是有些变量初始化以后，我们只想让他们在每个线程中一直存在，相当于一个线程内的共享变量，线程之间又是隔离的。 python threading模块中就提供了这么一个类，叫做local。local是一个小写字母开头的类，用于管理 thread-local（线程局部的）数据。对于同一个local，线程无法访问其他线程设置的属性；线程设置的属性不会被其他线程设置的同名属性替换。

可以把local看成是一个“线程-属性字典”的字典，local封装了从自身使用线程作为 key检索对应的属性字典、再使用属性名作为key检索属性值的细节。

