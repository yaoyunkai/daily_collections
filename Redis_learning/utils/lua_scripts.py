"""
Lua 示例


Created at 2023/3/25
"""
import redis

lua_demo1 = """
return 'Hello, scripting!'
"""

lua_demo2 = """
return ARGV[1]
"""

lua_demo3 = """
return { KEYS[1], KEYS[2], ARGV[1], ARGV[2], ARGV[3] }
"""

lua_demo4 = """return redis.call('SET', KEYS[1], ARGV[1])"""


def test_send_command():
    """
    redis> EVAL "return ARGV[1]" 0 Hello
    "Hello"
    redis> EVAL "return ARGV[1]" 0 Parameterization!
    "Parameterization!"

    """
    conn = redis.Redis()
    ret = conn.eval(lua_demo1, 0)
    print(ret)

    ret = conn.eval(lua_demo2, 0, 'hello world')
    print(ret)
    ret = conn.eval(lua_demo2, 0, 'hello Lua')
    print(ret)

    ret = conn.eval(lua_demo3, 2, 'key1', 'key2', 'dm1', 'dm2', 'dm4', 'dm5')
    print(ret)

    ret = conn.eval(lua_demo4, 1, 'foo', 'bar')
    print(ret)

    ret = conn.get('foo')
    print(ret)

    ret = conn.script_load(lua_demo3)
    print(ret)
    ret = conn.evalsha(ret, 2, 'key1', 'key2', 'dm1', 'dm2', 'dm4', 'dm5')
    print(ret)


if __name__ == '__main__':
    test_send_command()
