from pathlib import Path

# from part3_files_and_dirs.gencat import gen_cat
# from part3_files_and_dirs.genopen import gen_open


def line_from_dir(filepat, dirname):
    names = Path(dirname).rglob(filepat)
    files = gen_open(names)
    lines = gen_cat(files)
    return lines


if __name__ == '__main__':
    pass
