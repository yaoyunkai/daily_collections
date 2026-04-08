"""
05_as_completed.py

as_completed 设置超时后，无法确定哪些任务仍然在运行


created at 2026-04-08
"""

import asyncio

import aiohttp
from utils import delay as func_delay


async def fetch_status(session, url, delay=0):
    await func_delay(delay)
    async with session.get(url) as result:
        return result.status


async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://example.com"
        fetchers = [
            fetch_status(session, url, 2),
            fetch_status(session, url, 0),
            fetch_status(session, url, 1),
            fetch_status(session, url, 4),
        ]
        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)


async def run_with_timeout():
    async with aiohttp.ClientSession() as session:
        url = "https://example.com"
        fetchers = [
            fetch_status(session, url, 2),
            fetch_status(session, url, 0),
            fetch_status(session, url, 1),
            fetch_status(session, url, 4),
        ]
        for finished_task in asyncio.as_completed(fetchers, timeout=3.5):
            try:
                result = await finished_task
                print(result)
            except asyncio.TimeoutError:
                print("got timeout error")

        for task in asyncio.all_tasks():
            print(task)


if __name__ == "__main__":
    asyncio.run(run_with_timeout())
