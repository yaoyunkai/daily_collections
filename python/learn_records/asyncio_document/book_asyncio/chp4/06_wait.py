"""
06_wait.py


gather, as_completed, 看到异常时，没有简单的方法可以取消已经在运行的任务。

created at 2026-04-08
"""

import asyncio
import logging

import aiohttp


async def fetch_status(session, url):
    async with session.get(url) as result:
        return result.status


async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "https://example.com")),
            asyncio.create_task(fetch_status(session, "https://example.com")),
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")
        for done_task in done:
            result = await done_task
            print(result)


async def run_with_exceptions():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, "https://www.example.com")
        bad_request = fetch_status(session, "python://bad")

        fetchers = [asyncio.create_task(good_request), asyncio.create_task(bad_request)]

        done, pending = await asyncio.wait(fetchers)
        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            # result = await done_task will throw an exception
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("Request got an exception", exc_info=done_task.exception())


if __name__ == "__main__":
    asyncio.run(run_with_exceptions())
