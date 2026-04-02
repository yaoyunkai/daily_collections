# import asyncio
# import sys
#
# import uvloop
#
#
# async def main():
#     # 获取当前正在运行的事件循环
#     loop = asyncio.get_running_loop()
#     print(f"当前使用的事件循环类型: {type(loop).__name__}")
#
#     # 模拟异步操作
#     await asyncio.sleep(1)
#     print("执行完毕！")
#
#
# if __name__ == "__main__":
#     if sys.version_info >= (3, 11):
#         with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
#             runner.run(main())
#     else:
#         uvloop.install()
#         asyncio.run(main())
