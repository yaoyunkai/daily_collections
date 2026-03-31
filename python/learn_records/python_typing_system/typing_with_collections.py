"""
集合类型

"""

from collections import defaultdict
from typing import Generic, TypedDict, TypeVar

AuthorToCountMapping = dict[str, int]


class Cookbook:
    author: str

    def __init__(self, author: str):
        self.author = author


def create_author_count_mapping(cookbooks: list["Cookbook"]) -> AuthorToCountMapping:

    counter = defaultdict(
        int,
    )
    for book in cookbooks:
        counter[book.author] += 1

    return counter


class Range(TypedDict):
    min: float
    max: float


class NutritionInformation(TypedDict):
    value: int
    unit: str
    confidenceRange95Percent: Range
    standardDeviation: float


class RecipeNutritionInformation(TypedDict):
    recipes_used: int
    calories: NutritionInformation
    fat: NutritionInformation
    protein: NutritionInformation
    carbs: NutritionInformation


def get_recipe_nutrition(val: RecipeNutritionInformation):
    part2 = val["calories"]
    range_of_min = part2["confidenceRange95Percent"]["min"]
    print(f"min of range is {range_of_min}")


"""

泛型 


"""

T = TypeVar("T")


def reverse(collections: list[T]) -> list[T]:
    return collections[::-1]


def get_first_element(list_: list[T]) -> T:
    if len(list_) < 1:
        raise IndexError("no such element")

    return list_[0]


Node = TypeVar("Node")
Edge = TypeVar("Edge")


class Graph(Generic[Node, Edge]):
    def __init__(self):
        self.edges: dict[Node, list[Edge]] = defaultdict(list)

    def add_relation(self, node: Node, to: Edge):
        self.edges[node].append(to)

    def get_relations(self, node: Node) -> list[Edge]:
        return self.edges[node]


class Stack(Generic[T]):
    def __init__(self) -> None:
        # 内部使用 T 来注解存储的数据
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()


def use_generic():
    int_stack = Stack[int]()
    int_stack.push(10)
    int_stack.push(20)
    # int_stack.push("sss")

    print(Stack.__parameters__)
    print(Graph.__parameters__)


if __name__ == "__main__":
    au1 = "tom"
    au2 = "bob"
    au3 = "peter"

    bk1 = Cookbook(au1)
    bk2 = Cookbook(au1)
    bk3 = Cookbook(au1)

    bk4 = Cookbook(au2)
    bk5 = Cookbook(au2)
    bk6 = Cookbook(au2)
    bk7 = Cookbook(au2)
    bk8 = Cookbook(au2)

    bk9 = Cookbook(au3)

    result = create_author_count_mapping([bk1, bk2, bk3, bk4, bk5, bk6, bk7, bk8, bk9])
    print(result)

    # get_first_element(None)
    get_first_element([89])
    use_generic()
