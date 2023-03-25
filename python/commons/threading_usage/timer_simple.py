"""


Created at 2023/2/18
"""

import threading
import time


def func(num):
    print('hello {} timer!'.format(num))


# 如果t时候启动的函数是含有参数的，直接在后面传入参数元组
timer = threading.Timer(5, func, (1,))
time0 = time.time()
timer.start()
print(time.time() - time0)
