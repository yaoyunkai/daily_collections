loglines = open("../part2_process_data/access-log.txt", encoding='utf8')

import re

logpats = r'(\S+) (\S+) (\S+) \[(.*?)\] ' \
          r'"(\S+) (\S+) (\S+)" (\S+) (\S+)'

logpat = re.compile(logpats)

groups = (logpat.match(line) for line in loglines)
tuples = (g.groups() for g in groups if g)

if __name__ == '__main__':
    for t in tuples:
        print(t)
