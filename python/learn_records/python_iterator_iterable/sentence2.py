"""
可迭代
迭代器


"""

import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text: str):
        self.text = text
        self.words = RE_WORD.findall(self.text)

    # def __getitem__(self, idx):
    #     return self.words[idx]
    #
    # def __len__(self):
    #     return len(self.words)

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        return SentenceIterator(self.words)


class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __repr__(self):
        return self

    def __next__(self):
        try:
            _word = self.words[self.index]
        except IndexError:
            raise StopIteration

        self.index += 1
        return _word


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    print(s)
    for word in s:
        print(word)
