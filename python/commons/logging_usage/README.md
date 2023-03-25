# Logging

- `Logger`暴露了应用程序代码直接使用的接口。
- `Handler`将日志记录（由记录器创建）发送到适当的目标。
- `Filter`提供了更细粒度的功能，用于确定要输出的日志记录。
- `Formatter`指定最终输出中日志记录的样式。

```
%(name)s            Name of the logger (logging channel)
%(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                    WARNING, ERROR, CRITICAL)
%(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                    "WARNING", "ERROR", "CRITICAL")
%(pathname)s        Full pathname of the source file where the logging
                    call was issued (if available)
%(filename)s        Filename portion of pathname
%(module)s          Module (name portion of filename)
%(lineno)d          Source line number where the logging call was issued
                    (if available)
%(funcName)s        Function name
%(created)f         Time when the LogRecord was created (time.time()
                    return value)
%(asctime)s         Textual time when the LogRecord was created
%(msecs)d           Millisecond portion of the creation time
%(relativeCreated)d Time in milliseconds when the LogRecord was created,
                    relative to the time the logging module was loaded
                    (typically at application startup time)
%(thread)d          Thread ID (if available)
%(threadName)s      Thread name (if available)
%(process)d         Process ID (if available)
%(message)s         The result of record.getMessage(), computed just as
                    the record is emitted
```

## Class Info

- Logger
- Handler
- Formatter
- Filter
- LogRecord

日志处理流程:

![img](.assets/logging_flow.png)

1, For Logger

```
setLevel
addHandler 
addFilter

logger.error
logger.exception

getLogger
```

2, For Handler

```
setLevel
setFormatter
addFilter

```

3, For Formatter

### 配置日志记录

```
使用调用上面列出的配置方法的 Python 代码显式创建记录器、处理器和格式器。
创建日志配置文件并使用 fileConfig() 函数读取它。
创建配置信息字典并将其传递给 dictConfig() 函数。
```

### 传递给日志服务器

### 在自己的输出日志中添加上下文信息

可以使用过滤器传递上下文信息:

```python
import logging
from random import choice

class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    Rather than use actual contextual information, we just use random
    data in this demo.
    """

    USERS = ['jim', 'fred', 'sheila']
    IPS = ['123.231.231.123', '127.0.0.1', '192.168.0.1']

    def filter(self, record):

        record.ip = choice(ContextFilter.IPS)
        record.user = choice(ContextFilter.USERS)
        return True

if __name__ == '__main__':
    levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)-15s %(name)-5s %(levelname)-8s IP: %(ip)-15s User: %(user)-8s %(message)s')
    a1 = logging.getLogger('a.b.c')
    a2 = logging.getLogger('d.e.f')

    f = ContextFilter()
    a1.addFilter(f)
    a2.addFilter(f)
    a1.debug('A debug message')
    a1.info('An info message with %s', 'some parameters')
    for x in range(10):
        lvl = choice(levels)
        lvlname = logging.getLevelName(lvl)
        a2.log(lvl, 'A message at %s level with %d %s', lvlname, 2, 'parameters')
```

### 轮换日志文件

```python
import glob
import logging
import logging.handlers

LOG_FILENAME = 'logging_rotatingfile_example.out'

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20, backupCount=5)

my_logger.addHandler(handler)

# Log some messages
for i in range(20):
    my_logger.debug('i = %d' % i)

# See what files are created
logfiles = glob.glob('%s*' % LOG_FILENAME)

for filename in logfiles:
    print(filename)
```

## Django中的logging

django使用字典配置，默认配置如下：

```python
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
```

1, log处理过程中，第一次filter是Logger.filter, 第二次filter是 Handler.filter，那么两次filter的目的是什么？为了让不同的handler来决定是否处理这个log。

2, 如果自己要求自定义配置：可以把django配置copy过来。在源码里面，如果是dev模式，logging会配置两次，Logger对象的实例不变，但是对应的filters和handlers会被重新实例化。

3, logging模块在多进程下，同一个FileHandler写入文件的问题??? 是否可以根据进程号来修改文件名????

好像有问题 文件名会非常多??? 在uwsgi apache ... 等服务器部署时是不是思考用logger server的方式来进行。

当使用 [Gunicorn](https://gunicorn.org/) 或 [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) (或其他类似工具) 来部署 Web 应用时，会创建多个工作进程来处理客户端请求。 在这种环境下，要避免在你的 Web 应用中直接创建基于文件的处理句柄。 而应改为使用一个 [`SocketHandler`](https://docs.python.org/zh-cn/3/library/logging.handlers.html#logging.handlers.SocketHandler) 将来自 Web 应用的日志发送到在单独进程中运行的监听器。

4, 在Handler的filter中，可以通过额外的参数来判断是否记录到文件中，或者进行其他操作。

```python
get_logger_details(logging.root)
for k, v in logging.root.manager.loggerDict.items():
    if isinstance(v, logging.Logger):
        get_logger_details(v)

def get_logger_details(logger_obj):
    _str = 'Logger: {} -- {}\n'.format(logger_obj.name, id(logger_obj))
    if logger_obj.filters:
        _str += '   filters: '
        _str += ', '.join([str(i) for i in logger_obj.filters])
        _str += '\n'

    if logger_obj.handlers:
        for _idx, _h in enumerate(logger_obj.handlers):
            _str += '   {}. {} - {}\n'.format(_idx, _h, id(_h))
            if _h.filters:
                _str += '      filters: '
                _str += ', '.join([str(i) for i in _h.filters])
                _str += '\n'

    _str += '\n'
    print(_str, end='')
```

