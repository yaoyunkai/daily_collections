"""

二叉搜索树

created at 2025/4/15
"""
from typing import Optional


class TreeNode:
    def __init__(self, key, value, *, left=None, right=None, size=0):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.size = size

    def __str__(self):
        return f'Node<{self.key}>'


def _size(node: TreeNode):
    if node is None:
        return 0
    else:
        return node.size


def _get(node: TreeNode, key):
    if key is None:
        raise ValueError('calls get() with a null key')
    if node is None:
        return None

    if key == node.key:
        return node.value
    elif key < node.key:
        return _get(node.left, key)
    else:
        return _get(node.right, key)


def _put(x: TreeNode, key, value):
    """
    最终 x != null 还是返回x
    x == null 构造一个新的结点
    如果子树不为null会一直向下寻找, 比较每个子树的key

    key == k  update v
    key < k  x.left
    key > k  x.right

    """
    if x is None:
        return TreeNode(key, value, size=1)

    if key == x.key:
        x.value = value
    elif key < x.key:
        x.left = _put(x.left, key, value)
    else:
        x.right = _put(x.right, key, value)
    x.size = 1 + _size(x.left) + _size(x.right)
    return x


def _min(x: TreeNode):
    if x.left is None:
        return x
    else:
        return _min(x.left)


def _max(x: TreeNode):
    if x.right is None:
        return x
    else:
        return _max(x.right)


def _delete_min(x: TreeNode):
    """
    对于deleteMin()，我们要不断深入根结点的左子树中直至遇见一个空链接，
    然后将指向该结点的链接指向该结点的右子树（只需要在递归调用中返回它的右链接即可）

    """
    if x.left is None:
        return x.right
    x.left = _delete_min(x.left)
    x.size = _size(x.left) + _size(x.right) + 1
    return x


def _delete_max(x: TreeNode):
    if x.right is None:
        return x.left
    x.right = _delete_min(x.right)
    x.size = _size(x.left) + _size(x.right) + 1
    return x


def _delete(x: TreeNode, key):
    """
    对于只有一个子结点的删除方式，类似于 deleteMin or deleteMax
    当找到某个结点时, 子结点可能得情况 left right all null
                                  left right all not null  对于1,2种情况 if 一定成立
                                  left or right null

    对于有两个子结点的删除方式:
    在删除结点x后用它的后继结点填补它的位置。
    因为x有一个右子结点，因此它的后继结点就是其右子树中的最小结点。
    这样的替换仍然能够保证树的有序性，因为x.key和它的后继结点的键之间不存在其他的键。

    """
    if x is None:
        return None
    if key < x.key:
        x.left = _delete(x.left, key)
    elif key > x.key:
        x.right = _delete(x.right, key)
    else:
        #  只有一个子结点的情况, 巧妙的排他法
        if x.right is None:
            return x.left
        if x.left is None:
            return x.right
        # 在右子树中寻找最小的, 删除最小的，并把这个最小的填补到当前x的位置
        tmp = x
        # 现在x为右子树中最小的结点
        x = _min(tmp.right)

        #  现在 t.right 看作root, 因为最小结点即将变换位置, 所以删除他 从右子树中移除
        #  然后把右子树放回到 x.right
        x.right = _delete_min(tmp.right)

        #  连上要被删除的结点的左结点
        x.left = tmp.left

    x.size = _size(x.left) + _size(x.right) + 1
    return x


class BinarySearchTree:
    """
    Get
    Put
    Delete
    Len
    In


    """

    def __init__(self):
        self.root: Optional[TreeNode] = None

    def __len__(self):
        return self.size()

    def __contains__(self, item):
        return self.get(item) is not None

    def size(self):
        return _size(self.root)

    def is_empty(self):
        return self.size() == 0

    def get(self, key):
        return _get(self.root, key)

    def put(self, key, value):
        if key is None:
            raise ValueError('calls put() with a null key')
        if value is None:
            self.delete(key)

        self.root = _put(self.root, key, value)

    def min_key(self):
        return _min(self.root).key

    def max_key(self):
        return _max(self.root).key

    def delete(self, key):
        if key is None:
            raise ValueError('calls put() with a null key')
        self.root = _delete(self.root, key)

    def delete_min(self):
        if self.is_empty():
            raise ValueError('Symbol table underflow')
        self.root = _delete_min(self.root)

    def delete_max(self):
        if self.is_empty():
            raise ValueError('Symbol table underflow')
        self.root = _delete_max(self.root)


if __name__ == '__main__':
    bst = BinarySearchTree()
    bst.put(70, 1)
    bst.put(31, 1)
    bst.put(93, 1)
    bst.put(94, 1)
    bst.put(14, 1)
    bst.put(23, 1)
    bst.put(73, 1)

    print(len(bst))

    # bst.delete_min()
    # print(len(bst))

    print(bst.max_key())
    print(bst.min_key())

    bst.delete(14)
    print(bst)
