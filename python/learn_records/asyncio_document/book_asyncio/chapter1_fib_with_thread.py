import threading
import time


def print_fib(number: int) -> None:
    def fib(n: int) -> int:
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)

    print(f'fib({number}) is {fib(number)}')


def fibs_with_threading():
    t1 = threading.Thread(target=print_fib, args=(40,))
    t2 = threading.Thread(target=print_fib, args=(41,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


start = time.time()

fibs_with_threading()

end = time.time()

print(f'Completed in {end - start:.4f} seconds.')
