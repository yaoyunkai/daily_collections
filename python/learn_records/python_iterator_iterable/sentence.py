import random
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text: str):
        self.text = text
        self.words = RE_WORD.findall(self.text)

    def __getitem__(self, idx):
        return self.words[idx]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'


def d6():
    return random.randint(1, 6)


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    print(s)
    # for word in s:
    #     print(word)

    it = iter(s)
    print(it)
    print(type(it))

    # for a in it:
    #     print(a)

    # while True:
    #     try:
    #         res = next(it)
    #         print(res)
    #     except StopIteration:
    #         break

    d6_iter = iter(d6, 1)

    for roll in d6_iter:
        print(roll)
