"""

任意一秒创建一个打印任务的概率:
每小时20 -> 每180s 1个任务。通过1-180的随机数来模拟每秒内产生打印任务的概率。


created at 2025/1/10
"""

import random

from linkedlist_queue import Queue


class Printer:
    def __init__(self, ppm):
        self.page_rate = ppm
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task is not None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        return self.current_task is not None

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = self.current_task.get_pages() * 60 / self.page_rate


class Task:
    def __init__(self, time_):
        self.timestamp = time_
        self.pages = random.randrange(1, 21)

    def get_stamp(self):
        return self.timestamp

    def get_pages(self):
        return self.pages

    def wait_time(self, current_time):
        return current_time - self.timestamp


def simulation(num_seconds, pages_per_minute):
    lab_printer = Printer(pages_per_minute)
    print_queue = Queue()
    waiting_times = []

    for current_second in range(num_seconds):
        if new_print_task():
            task = Task(current_second)
            print_queue.enqueue(task)

        if not lab_printer.busy() and not print_queue.is_empty():
            next_task = print_queue.dequeue()
            waiting_times.append(next_task.wait_time(current_second))
            lab_printer.start_next(next_task)

        lab_printer.tick()

    avg_wait = sum(waiting_times) / len(waiting_times)
    print(f'average wait {avg_wait:.2f} seconds, {print_queue.size()} tasks remaining.')


def new_print_task():
    num = random.randrange(1, 181)
    return num == 180


if __name__ == '__main__':
    simulation(3600, 5)
