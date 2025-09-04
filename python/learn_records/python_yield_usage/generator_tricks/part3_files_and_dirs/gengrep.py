import re


def gen_grep(pat, lines):
    patc = re.compile(pat)
    return (line for line in lines if patc.search(line))
