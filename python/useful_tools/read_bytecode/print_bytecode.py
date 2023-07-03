"""
Created at 2023/7/2


"""
import dis
import os


def get_bytecode(filepath):
    """
    filepath 是否是一个文件
    filepath 是否可以打开
    filepath 是不是真的是python的代码
    
    :param filepath: 
    :return: 
    """

    fp = None
    try:
        fp = open(filepath, mode='r')
        co = compile(fp.read(), os.path.basename(filepath), 'exec')
        dis.dis(co)
    except OSError as e:
        print(f'open file fatal error: {e}')
    finally:
        if fp:
            fp.close()


if __name__ == '__main__':
    # print(os.path.basename('/sdf/sdf/demo.txt'))
    # print(os.path.basename('.demo.txt'))
    # print(os.path.basename('./.demo.txt'))

    get_bytecode('for_bytecode_demo1.py')
