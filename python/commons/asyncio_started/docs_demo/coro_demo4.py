"""

asyncio.create_task
asyncio.ensure_future


Created at 2023/4/8
"""
import asyncio


async def coro():
    pass


# In Python 3.7+
task1 = asyncio.create_task(coro())

# This works in all Python versions but is less readable
task2 = asyncio.ensure_future(coro())
