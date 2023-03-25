# lua in redis

在 Redis 中，执行 Lua 脚本的时候，其他客户端可以执行命令，因为 Redis 的 Lua 脚本是原子性执行的。当一个客户端执行 Lua 脚本时，Redis 会将该脚本作为一个整体执行，这意味着在执行期间，Redis 会将所有命令和脚本中的命令原子地执行，而不允许其他客户端进行操作。

在执行 Lua 脚本期间，Redis 会将所有的客户端操作缓存起来，等到脚本执行完成后再将它们执行。在脚本执行期间，Redis 会阻塞其他客户端的所有操作，直到脚本执行完成。这确保了 Lua 脚本的原子性和数据的一致性。

需要注意的是，Redis 仍然允许其他客户端发送命令，但是这些命令会在脚本执行完成后才会被执行。这意味着其他客户端的操作可能会被延迟，直到脚本执行完成。因此，在编写 Lua 脚本时，应该尽量避免长时间的脚本执行，以免影响其他客户端的操作。

---

Redis保证了脚本的原子执行。在执行脚本时，所有服务器活动在整个运行时都被阻塞。这些语义意味着脚本的所有效果要么还没有发生，要么已经发生。

脚本编写提供了一些在许多情况下都很有价值的属性。这些包括:

- 通过在数据所在的地方执行逻辑来提供局部性。 数据局部性减少了整体延迟并节省了网络资源。
- 确保脚本原子执行的阻塞语义。
- 启用 Redis 中缺少的或过于小众的简单功能的组合。

虽然服务器执行它们，但 Eval 脚本被视为客户端应用程序的一部分，这就是它们没有命名、版本化或持久化的原因。 因此，如果所有脚本丢失，应用程序可能需要随时重新加载（在服务器重启、故障转移到副本等之后）。

## get start

`EVAL script numkeys [key [key ...]] [arg [arg ...]]`

使用EVAL命令：

```
> EVAL "return 'Hello, scripting!'" 0
"Hello, scripting!"
```

参数化脚本：

```
redis> EVAL "return ARGV[1]" 0 Hello
"Hello"
redis> EVAL "return ARGV[1]" 0 Parameterization!
"Parameterization!"
```

重要提示：为了确保在独立部署和集群部署中正确执行脚本，脚本访问的所有键名都必须作为输入键参数显式提供。 该脚本应该只访问其名称作为输入参数给出的键。 脚本永远不应访问具有以编程方式生成的名称或基于存储在数据库中的数据结构的内容的密钥。

## call redis command

- `redis.call()`
- `redis.pcall()`

两者几乎一模一样。 两者都执行 Redis 命令及其提供的参数（如果这些参数表示格式正确的命令）。

但是，这两个函数之间的区别在于处理运行时错误（例如语法错误）的方式。 调用 redis.call() 函数引发的错误会直接返回给执行它的客户端。 相反，调用 redis.pcall() 函数时遇到的错误将返回到脚本的执行上下文，而不是进行可能的处理。

## script cache

每当我们调用 EVAL 时，我们还会在请求中包含脚本的源代码。 重复调用 EVAL 执行同一组参数化脚本，既浪费了网络带宽，也对 Redis 产生了一些开销。 当然，节省网络和计算资源是关键，因此，Redis 为脚本提供了一种缓存机制。

您使用 EVAL 执行的每个脚本都存储在服务器保留的专用缓存中。 缓存的内容由脚本的 SHA1 摘要总和组织，因此脚本的 SHA1 摘要总和在缓存中唯一标识它。 您可以通过运行 EVAL 并随后调用 INFO 来验证此行为。 您会注意到 `used_memory_scripts_eval` 和 `number_of_cached_scripts` 指标随着执行的每个新脚本而增长。

- script load - 生成sha值
- evasha - 通过给定的sha值执行脚本

```
redis> SCRIPT LOAD "return 'Immabe a cached script'"
"c664a3bf70bd1d45c4284ffebb65a6f2299bfc9f"
redis> EVALSHA c664a3bf70bd1d45c4284ffebb65a6f2299bfc9f 0
"Immabe a cached script"
```

Redis 脚本缓存始终是易变的。 它不被视为数据库的一部分，也不会持久化。 缓存可能会在服务器重新启动时被清除，在故障转移期间当副本承担主角色时，或者由 `SCRIPT FLUSH` 显式清除。 这意味着缓存的脚本是短暂的，缓存的内容随时可能丢失。

## EVALSHA in the context of pipelining

在流水线请求的上下文中执行 EVALSHA 时应特别小心。 流水线请求中的命令按它们发送的顺序运行，但其他客户端的命令可能会交错执行。 因此，NOSCRIPT 错误可以从流水线请求返回但无法处理。

因此，客户端库的实现应该恢复到在管道上下文中使用普通的`EVAL`

## 脚本相关命令

- script flush - 清空脚本缓存
- script exists - 给定一个或多个 SHA1 摘要作为参数，此命令返回一个由1和0组成的数组。1表示特定的 SHA1 被识别为已存在于脚本缓存中的脚本。
- script load
- script kill 
- script debug

## Global variables and functions

在redis的Lua脚本中，不能定义全局的变量或者方法：

```lua
my_global_variable = 'some value'

function my_global_function()
  -- Do something amazing
end

-- The following will surely raise an error
return an_undefined_global_variable
```

相反，所有变量和函数定义都必须声明为局部的。

```lua
local my_local_variable = 'some value'

local function my_local_function()
  -- Do something else, but equally amazing
end
```

## Runtime globals

- redis object
- KEYS
- ARGV

### redis object

Redis Lua执行上下文总是提供一个名为Redis的对象的单例实例。redis实例允许脚本与运行它的redis服务器交互。下面是redis对象实例提供的API。

```
redis.call(command [,arg...])

redis.pcall(command [,arg...])

redis.error_reply(x)

redis.status_reply(x)

redis.sha1hex(x)

redis.log(level, message)
redis.LOG_DEBUG
redis.LOG_VERBOSE
redis.LOG_NOTICE
redis.LOG_WARNING

redis.setresp(x)

redis.set_repl(x)

redis.replicate_commands()

redis.breakpoint()

redis.debug(x)

redis.acl_check_cmd(command [,arg...])

redis.register_function


```

## Data Conversion

## redis 可以使用lua module