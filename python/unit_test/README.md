# 单元测试

单元测试的相关概念：

**测试脚手架**：*test fixture* 表示为了开展一项或多项测试所需要进行的准备工作，以及所有相关的清理操作。举个例子，这可能包含创建临时或代理的数据库、目录，再或者启动一个服务器进程。

**测试用例**：一个测试用例是一个独立的测试单元。它检查输入特定的数据时的响应。 [unittest](https://docs.python.org/zh-cn/3/library/unittest.html#module-unittest) 提供一个基类： [TestCase](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase) ，用于新建测试用例。

**测试套件**：*test suite* 是一系列的测试用例，或测试套件，或两者皆有。它用于归档需要一起执行的测试。

**测试运行器（test runner）**: *test runner* 是一个用于执行和输出测试结果的组件。这个运行器可能使用图形接口、文本接口，或返回一个特定的值表示运行测试的结果。

## 基本用例

```python
import unittest


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
```

调用 [assertEqual()](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertEqual) 来检查预期的输出； 调用 [assertTrue()](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertTrue) 或 [assertFalse()](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertFalse) 来验证一个条件；调用 [assertRaises()](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.assertRaises) 来验证抛出了一个特定的异常。

通过 [setUp()](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.setUp) 和 [tearDown()](https://docs.python.org/zh-cn/3/library/unittest.html#unittest.TestCase.tearDown) 方法，可以设置测试开始前与完成后需要执行的指令。

## 命令行接口

unittest 模块可以通过命令行运行模块、类和独立测试方法的测试:

```
python -m unittest test_module1 test_module2
python -m unittest test_module.TestClass
python -m unittest test_module.TestClass.test_method
```

你可以传入模块名、类或方法名或他们的任意组合。

同样的，测试模块可以通过文件路径指定:

```
python -m unittest tests/test_something.py
```

### 命令行选项

```
-b, --buffer: 标准输出和标准错误流在测试运行期间被缓冲。通过测试时的输出将被丢弃。在测试失败或错误时，输出将正常显示，并添加到失败消息中。

-c, --catch: 

-f, --failfast: 快速失败

-k: 匹配测试用例

--locals: Show local variables in tracebacks.
```

## Test Discovery

## 组织测试代码

一般来说会继承TestCase类，每个TestCase类会有很多以test_开头的测试方法。

```python
import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()
```

If `setUp()` succeeded, `tearDown()` will be run whether the test method succeeded or not.

这样的一个测试代码运行的环境被称为 `test fixture` 。一个新的 TestCase 实例作为一个测试脚手架，用于运行各个独立的测试方法。在运行每个测试时，`setUp()` 、`tearDown()` 和 `__init__()` 会被调用一次。

然而，如果你需要自定义你的测试套件的话，你可以参考以下方法组织你的测试：

```python
def suite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase('test_default_widget_size'))
    suite.addTest(WidgetTestCase('test_widget_resize'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
```
