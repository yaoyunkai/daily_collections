"""
Gen cat


"""


def gen_cat(sources):
    for src in sources:
        yield from src


if __name__ == '__main__':
    from genfind import gen_find
    from genopen import gen_open

    log_names = gen_find('access-log*', r'C:\Users\libyao\Downloads\www')
    log_files = gen_open(log_names)
    log_lines = gen_cat(log_files)

    for line in log_lines:
        print(line)
