import re

from fieldmap import field_map

logpats = r'(\S+) (\S+) (\S+) \[(.*?)\] ' \
          r'"(\S+) (\S+) (\S+)" (\S+) (\S+)'

logpat = re.compile(logpats)


def apache_log(lines):
    groups = (logpat.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)

    colnames = ('host', 'referrer', 'user', 'datetime',
                'method', 'request', 'proto', 'status', 'bytes')

    log = (dict(zip(colnames, t)) for t in tuples)
    log = field_map(log, "status", int)
    log = field_map(log, "bytes", lambda s: int(s) if s != '-' else 0)

    return log


if __name__ == '__main__':
    pass
