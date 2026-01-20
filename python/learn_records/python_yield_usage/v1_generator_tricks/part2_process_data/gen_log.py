"""
Gen log

data processing pipeline

file -> file object -> columns -> bytes_sent -> sum -> result

迭代是数据处理的关键
pipeline的拆分和模块化


"""


def run():
    with open("access-log.txt") as wwwlog:
        bytecolumn = (line.rsplit(None, 1)[1] for line in wwwlog)
        bytes_sent = (int(x) for x in bytecolumn if x != '-')
        print("Total", sum(bytes_sent))


if __name__ == '__main__':
    run()
