"""
位置参数
默认参数，默认参数必须放在位置参数之后。
关键字参数
可变长度位置参数   *args
可变长度关键字参数   **kwargs
强制关键字参数 (Keyword-Only Arguments)  使用星号 * 分隔，星号之后的参数在调用时必须使用关键字形式传递。
强制位置参数 (Positional-Only Arguments)  在 / 之前的参数必须通过位置传递，不能使用关键字。


"""


def greet(name, age):
    print(f"你好 {name}，你今年 {age} 岁。")


greet("Alice", 25)  # 正确


def greet(name, msg="欢迎"):
    print(f"{name}, {msg}")


greet("Bob")  # 输出: Bob, 欢迎
greet("Bob", "早安")  # 输出: Bob, 早安


def describe_pet(animal_type, pet_name):
    print(f"我有一只 {animal_type}，名字叫 {pet_name}。")


describe_pet(pet_name="哈利", animal_type="狗")


def sum_numbers(*args):
    return sum(args)


print(sum_numbers(1, 2, 3, 4))  # 输出: 10
