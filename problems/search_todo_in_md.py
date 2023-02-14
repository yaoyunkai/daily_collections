"""
Search todos in Markdown file

get current line for todos

return result:

file_name lines: todo_string, then generate a file with datetime save them all in one place


"""

import re

TODO_PT = re.compile(r'^> (?:TODO|todo): (.*?)$')

demo = '> TODO: 简单case和搜索case的区别???'


def test():
    results = TODO_PT.findall(demo)
    print(results)


if __name__ == '__main__':
    test()
