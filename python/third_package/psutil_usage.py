"""


created at 2024/9/29
"""

import psutil


def list_processes():
    for proc in psutil.process_iter():
        print(proc)


if __name__ == '__main__':
    list_processes()
