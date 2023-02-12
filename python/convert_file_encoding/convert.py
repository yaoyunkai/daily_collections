"""
文本文件格式转换


"""
import os

import chardet


def convert_encoding(file_path):
    """
    convert file encoding to utf8

    :param file_path:
    :return:
    """
    with open(file_path, mode='rb') as fp:
        orig_blob = fp.read()

    detection = chardet.detect(orig_blob)
    encoding = detection['encoding']

    if not encoding:
        raise TypeError('can\'t guess file encoding: {}'.format(file_path))

    try:
        fp = open(file_path, mode='wb')
        fp.write(orig_blob.decode(encoding, errors='replace').encode('utf8'))
        fp.close()
    except Exception as e:
        print(e)
        print('meet error when write file: {}'.format(file_path))


def deal_dirs(dir_path):
    """

    :param dir_path: should be absolute path
    :return:
    """
    if os.path.isdir(dir_path):
        for _next_path in os.listdir(dir_path):
            full_path = os.path.join(dir_path, _next_path)
            if os.path.isdir(full_path):
                deal_dirs(full_path)
            elif os.path.isfile(full_path):
                convert_encoding(full_path)
            else:
                print('skipped deal with the path: {}'.format(full_path))


if __name__ == '__main__':
    root_path = r'D:\projects\code\python\demo1\collection\python\convert_file_encoding\root'
    deal_dirs(root_path)
