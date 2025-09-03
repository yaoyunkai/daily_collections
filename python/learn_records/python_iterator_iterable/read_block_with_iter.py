from functools import partial

with open('random.txt', mode='r', encoding='utf8') as f:
    read_block = partial(f.read, 4)
    for block in iter(read_block, ''):
        print(block)
