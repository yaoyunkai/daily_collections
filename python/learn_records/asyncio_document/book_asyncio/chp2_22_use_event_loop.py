"""
chp2_22_use_event_loop.py

created at 2026-04-07
"""

import asyncio

from utils import delay


def call_later():
    print("I am being called in the future")


async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)


asyncio.run(main())
