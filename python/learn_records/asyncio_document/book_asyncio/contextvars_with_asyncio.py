"""
contextvars_with_asyncio.py


created at 2026-04-23
"""

import asyncio
import contextvars

request_id = contextvars.ContextVar("Id of request")


async def get():
    print(f"request id get: {request_id.get()}")


async def new_coro(req_id):
    request_id.set(req_id)
    await get()
    print(f"request id set: {request_id.get()}")


async def main():
    tasks = []
    for req_id in range(1, 5):
        tasks.append(asyncio.create_task(new_coro(req_id)))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
