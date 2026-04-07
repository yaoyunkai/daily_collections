"""
chp2_20_with_requests.py

created at 2026-04-07
"""

import asyncio

import requests
from utils import async_timed


@async_timed()
async def get_resp_status_code():
    return requests.get("http://www.example.com").status_code


@async_timed()
async def main():
    task1 = asyncio.create_task(get_resp_status_code())
    task2 = asyncio.create_task(get_resp_status_code())
    task3 = asyncio.create_task(get_resp_status_code())

    await task1
    await task2
    await task3


if __name__ == "__main__":
    asyncio.run(main())
