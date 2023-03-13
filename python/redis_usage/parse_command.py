"""
将redis 命令转换为 RESP spec


Created at 2023/3/8
"""

from hiredis import pack_command as hi_pack_command

SYM_STAR = b'*'
SYM_DOLLAR = b'$'
SYM_CRLF = b'\r\n'
SYM_EMPTY = b''


def encode(value):
    """
    Return a bytestring or bytes-like representation of the value

    """
    if isinstance(value, (bytes, memoryview)):
        return value
    elif isinstance(value, bool):
        # special case bool since it is a subclass of int
        raise ValueError("Invalid input of type: 'bool'. Convert to a "
                         "bytes, string, int or float first.")
    elif isinstance(value, float):
        value = repr(value).encode()
    elif not isinstance(value, str):
        # a value we don't know how to deal with. throw an error
        typename = type(value).__name__
        raise ValueError("Invalid input of type: '%s'. Convert to a "
                         "bytes, string, int or float first." % typename)
    if isinstance(value, str):
        value = value.encode('utf8', 'strict')
    return value


def pack_command(*args):
    """Pack a series of arguments into the Redis protocol"""
    output = []
    # the client might have included 1 or more literal arguments in
    # the command name, e.g., 'CONFIG GET'. The Redis server expects these
    # arguments to be sent separately, so split the first argument
    # manually. These arguments should be bytestrings so that they are
    # not encoded.
    if isinstance(args[0], str):
        args = tuple(args[0].encode().split()) + args[1:]
    elif b' ' in args[0]:
        args = tuple(args[0].split()) + args[1:]

    buff = SYM_EMPTY.join((SYM_STAR, str(len(args)).encode(), SYM_CRLF))

    buffer_cutoff = 6000
    for arg in map(encode, args):
        # to avoid large string mallocs, chunk the command into the
        # output list if we're sending large values or memoryviews
        arg_length = len(arg)
        if (len(buff) > buffer_cutoff or arg_length > buffer_cutoff
                or isinstance(arg, memoryview)):
            buff = SYM_EMPTY.join(
                (buff, SYM_DOLLAR, str(arg_length).encode(), SYM_CRLF))
            output.append(buff)
            output.append(arg)
            buff = SYM_CRLF
        else:
            buff = SYM_EMPTY.join(
                (buff, SYM_DOLLAR, str(arg_length).encode(),
                 SYM_CRLF, arg, SYM_CRLF))
    output.append(buff)
    return output


if __name__ == '__main__':
    # print(pack_command('SET', 'name', 'tom'))
    print(pack_command('SET', 'name', '你好'))
    print(hi_pack_command(('SET', 'name', '你好')))

    import timeit

    res1 = timeit.timeit("""pack_command('SET', 'name', '你好')""", number=1000000, globals=globals())
    res2 = timeit.timeit("""hi_pack_command(('SET', 'name', '你好'))""", number=1000000, globals=globals())

    print(res1)
    print(res2)
