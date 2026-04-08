"""
04_gather.py

asyncio.gather -> awaitables object

return_exceptions

created at 2026-04-08
"""

import asyncio

import aiohttp
from utils import async_timed


@async_timed()
async def fetch_status(session, url):
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["https://example.com" for _ in range(50)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


@async_timed()
async def run_expections():
    async with aiohttp.ClientSession() as session:
        url1 = "https://example.com"
        url2 = url1.replace("https", "python")
        tasks = [fetch_status(session, url1), fetch_status(session, url2)]
        status_codes = await asyncio.gather(*tasks)
        print(status_codes)


async def run_return_expections():
    async with aiohttp.ClientSession() as session:
        url1 = "https://example.com"
        url2 = url1.replace("https", "python")
        tasks = [fetch_status(session, url1), fetch_status(session, url2)]
        status_codes = await asyncio.gather(*tasks, return_exceptions=True)
        for status_code in status_codes:
            if isinstance(status_code, Exception):
                print(f"error: {status_code}")
            else:
                print(f"passed: {status_code}")


if __name__ == "__main__":
    asyncio.run(run_return_expections())
