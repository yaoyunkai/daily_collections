# 什么时候使用Task ，什么时候使用Coroutine

**本质区别 (Fundamental Difference):**

- **Coroutine (协程对象):** 当你调用一个 `async def` 函数时（例如 `c = my_async_func()`），你得到的是一个协程对象。此时，**代码并没有开始执行**。
- **Task (任务对象):** 当你使用 `asyncio.create_task(c)` 包装一个协程时，你得到的是一个 Task。此时，这个协程被**正式注册到了事件循环 (Event Loop) 中，并安排在后台准备运行**。Task 就像是“正在照着菜谱做菜的厨师”。Task 是 `Future` 的子类，代表一个异步操作的最终结果。

**API 设计的初衷 (API Design Intent):**

- **为了“便捷” (Convenience):** 像 `asyncio.gather(*coros_or_futures)` 这样的高级 API，它的主要目的是“帮我把这些事做完并把结果按顺序给我”。为了方便开发者，它允许直接传入 `coro`。在底层，`gather` 会自动帮你把这些 `coro` 包装成 `Task` 并运行。
- **为了“控制” (Control):** 像 `asyncio.wait(fs)` 这样的底层/中级 API，它的目的是“状态管理”（区分哪些完成了，哪些还在运行）。如果你传给它一个 `coro`，它在内部包装成 `Task` 后，返回给你的 `done` 和 `pending` 集合里装的将是它内部生成的全新 `Task` 对象。由于你手里没有这些新 `Task` 的引用，你将无法对它们进行后续操作（比如取消 `task.cancel()`）。因此，Python 官方在较新的版本中（Python 3.8 弃用，3.11 移除），**强制要求** `asyncio.wait` 必须传入 `Task` 列表。

传入 `coro` 还是 `task` 的核心在于：**你是只需要“最终结果”（传 coro 即可，API 帮你代劳），还是需要对执行过程进行“精细化生命周期管理”（必须自己创建并传入 task）**。

最佳实践是：**只要你需要并发执行多个操作，就应该习惯性地使用 `asyncio.create_task()` 将它们包装为 Task**，然后再将这些 Task 传递给 `gather`、`wait` 或 `as_completed`。

