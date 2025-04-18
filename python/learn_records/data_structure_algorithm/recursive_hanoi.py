"""

汉诺塔
https://zh.wikipedia.org/wiki/%E6%B1%89%E8%AF%BA%E5%A1%94


created at 2025/4/10
"""


def move_tower(height, from_pole, to_pole, with_pole):
    if height >= 1:
        move_tower(height - 1, from_pole, with_pole, to_pole)
        move_disk(from_pole, to_pole)
        move_tower(height - 1, with_pole, to_pole, from_pole)


def move_disk(fp, tp):
    print(f'moving disk from {fp} to {tp} \n')
