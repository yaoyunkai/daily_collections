"""
Created at 2023/8/5


OPT_APPEND_NEWLINE              在末尾添加换行符
OPT_INDENT_2                    缩进2个空格
OPT_NAIVE_UTC                   将不带 tzinfo 的 datetime.datetime 对象序列化为 UTC。
OPT_NON_STR_KEYS                允许字典中的非字符串键
OPT_OMIT_MICROSECONDS           忽略 datetime.datetime 对象中的微秒
OPT_PASSTHROUGH_DATACLASS       将 dataclasses.dataclass 实例转为默认。这允许自定义其输出，但速度要慢得多。

OPT_PASSTHROUGH_DATETIME        将 datetime.datetime、datetime.date 和 datetime.time 实例转入默认值。
                                这样就可以将日期时间序列化为自定义格式
                                
OPT_PASSTHROUGH_SUBCLASS        禁止序列化 str int ...的子类
OPT_SERIALIZE_DATACLASS         已经被废弃
OPT_SERIALIZE_NUMPY             序列化 numpy.ndarray 和 numpy.number
OPT_SERIALIZE_UUID              序列化 uuid.UUID，已经被废弃
OPT_SORT_KEYS                   排序字典键
OPT_STRICT_INTEGER
OPT_UTC_Z



"""
import datetime
from json import dumps as json_dumps

from orjson import dumps as orjson_dumps

# generate a complex dict structure
val = {
    "a": 1,
    "b": 2,
    "c": {
        "d": 3,
        "e": 4,
        "f": {
            "g": 5,
            "h": 6,
            "j": 7,
        },
    },
}


def default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%a, %d %b %Y %H:%M:%S GMT")
    raise TypeError


ITER_COUNTS = 100000


def orjson_test():
    orjson_dumps(
        val,
    )


def json_test():
    json_dumps(
        val,
    )


def json_datetime():
    ret = orjson_dumps({"created_at": datetime.datetime(1970, 1, 1), "name": "bob"})
    print(ret.decode("utf8"))


if __name__ == "__main__":
    # import timeit
    #
    # rel1 = timeit.timeit(orjson_test, number=ITER_COUNTS)
    # rel2 = timeit.timeit(json_test, number=ITER_COUNTS)
    #
    # print(f"orjson: {rel1}")
    # print(f"json: {rel2}")

    json_datetime()
