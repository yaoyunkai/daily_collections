"""

read log bytes


"""


def run():
    total = 0

    with open('access-log.txt', mode='r', encoding='utf8') as fp:
        for line in fp:
            nbytes = line.rsplit(None, 1)[-1]
            if nbytes != '-':
                total += int(nbytes)
    print(f'Get {total} bytes')
    return total


if __name__ == '__main__':
    run()
