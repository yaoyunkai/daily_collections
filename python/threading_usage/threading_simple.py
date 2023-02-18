"""


Created at 2023/2/18
"""

import threading

a = 0
threads = []


def x():
    global a
    for i in range(1_000_000):
        a += 1


for _ in range(10):
    thread = threading.Thread(target=x)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(a)
