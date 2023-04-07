# inline2.py
#
# Inline future forumulation with exception handling added

class Task:
    def __init__(self, gen):
        self._gen = gen

    def step(self, value=None, exc=None):
        try:
            if exc:
                fut = self._gen.throw(exc)
            else:
                fut = self._gen.send(value)
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            pass

    def _wakeup(self, fut):
        try:
            result = fut.result()
            self.step(result, None)
        except Exception as exc:
            self.step(None, exc)


# Example
if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    import time

    pool = ThreadPoolExecutor(max_workers=8)


    def func(x, y):
        time.sleep(1)
        return x + y


    def after(delay, gen):
        """
        Run an inlined future after a time delay

        """
        yield pool.submit(time.sleep, delay)
        yield gen


    def after2(delay, gen):
        """
        Run an inlined future after a time delay

        """
        yield pool.submit(time.sleep, delay)
        for f in gen:
            yield f


    def after3(delay, gen):
        """
        Run an inlined future after a time delay

        """
        yield pool.submit(time.sleep, delay)
        result = None
        try:
            while True:
                f = gen.send(result)
                result = yield f
        except StopIteration:
            pass


    def after4(delay, gen):
        """
        Run an inlined future after a time delay

        """
        yield pool.submit(time.sleep, delay)
        yield from gen


    def do_func(x, y):
        try:
            result = yield pool.submit(func, x, y)
            print('Got:', result)
        except Exception as e:
            print('Failed:', repr(e))


    Task(after4(3, do_func(2, 3))).step()
