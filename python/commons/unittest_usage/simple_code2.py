import sys
import unittest

ABC = 1


class Demo2TestCase(unittest.TestCase):
    """
    这个类会被实例化两次???

    """

    def setUp(self):
        global ABC
        self._tmp = ABC
        ABC += 1

    def tearDown(self) -> None:
        # print('xxxxxx', file=sys.stderr)
        print(self._tmp, file=sys.stderr)
        print(id(self), file=sys.stderr)

    def test_a(self):
        self.assertTrue(1 == 1)

    def test_2(self):
        self.assertTrue(1 == 1)


if __name__ == '__main__':
    unittest.main()
