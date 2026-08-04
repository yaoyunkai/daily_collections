"""
primes_queue.py


created at 2026-08-04
"""

import argparse
import math
import multiprocessing
import time
from multiprocessing import Queue

FLAG_ALL_DONE = b"WORK_FINISHED"
FLAG_WORKER_FINISHED_PROCESSING = b"WORKER_FINISHED_PROCESSING"


def check_prime(possible_primes_queue: "Queue", definite_primes_queue: "Queue"):
    while True:
        num = possible_primes_queue.get()
        if num == FLAG_ALL_DONE:
            # flag that our results have all been pushed to the results queue
            definite_primes_queue.put(FLAG_WORKER_FINISHED_PROCESSING)
            break
        else:
            if num % 2 == 0:
                continue
            for i in range(3, int(math.sqrt(num)) + 1, 2):
                if num % i == 0:
                    break
            else:
                definite_primes_queue.put(num)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project description")
    parser.add_argument("nbr_workers", type=int, help="Number of workers e.g. 1, 2, 4, 8")
    args = parser.parse_args()
    print(args)

    primes = []

    manager = multiprocessing.Manager()
    p_q = manager.Queue()
    d_q = manager.Queue()

    processes = []

    for _ in range(args.nbr_workers):
        proc = multiprocessing.Process(target=check_prime, args=(p_q, d_q))
        processes.append(proc)
        proc.start()

    t1 = time.time()
    # number_range = xrange(100000000, 100010000)  # A
    # number_range = xrange(100000000, 100100000)  # B
    number_range = range(1000, 10000)  # C
    # number_range = xrange(1000000000, 1000100000)  # D
    # number_range = xrange(100000000000, 100000100000)  # E

    for possible_prime in number_range:
        p_q.put(possible_prime)
    print("ALL JOBS ADDED TO THE QUEUE")

    # add poison pills to stop the remote workers
    for n in range(args.nbr_workers):
        p_q.put(FLAG_ALL_DONE)

    print("NOW WAITING FOR RESULTS...")
    processors_indicating_they_have_finished = 0
    while True:
        new_result = d_q.get()  # block whilst waiting for results
        if new_result == FLAG_WORKER_FINISHED_PROCESSING:
            print("WORKER {} HAS JUST FINISHED".format(processors_indicating_they_have_finished))
            processors_indicating_they_have_finished += 1
            if processors_indicating_they_have_finished == args.nbr_workers:
                break
        else:
            primes.append(new_result)
    assert processors_indicating_they_have_finished == args.nbr_workers

    print("Took:", time.time() - t1)
    print(len(primes), primes[:10], primes[-10:])
