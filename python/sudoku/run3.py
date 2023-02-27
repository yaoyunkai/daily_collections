"""


Created at 2023/2/27
"""


def find_empty_location(puzzle, l):
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                l[0], l[1] = row, col
                return True
    return False


def used_in_row(puzzle, row, num):
    for col in range(9):
        if puzzle[row][col] == num:
            return True
    return False


def used_in_col(puzzle, col, num):
    for row in range(9):
        if puzzle[row][col] == num:
            return True
    return False


def used_in_box(puzzle, row, col, num):
    for i in range(3):
        for j in range(3):
            if puzzle[i + row][j + col] == num:
                return True
    return False


def is_valid_location(puzzle, row, col, num):
    return not used_in_row(puzzle, row, num) and not used_in_col(puzzle, col, num) and not used_in_box(puzzle,
                                                                                                       row - row % 3,
                                                                                                       col - col % 3,
                                                                                                       num)


def solve_puzzle(puzzle):
    l = [0, 0]
    if not find_empty_location(puzzle, l):
        return True
    row, col = l[0], l[1]
    for num in range(1, 10):
        if is_valid_location(puzzle, row, col, num):
            puzzle[row][col] = num
            if solve_puzzle(puzzle):
                return True
            puzzle[row][col] = 0
    return False


puzzle = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0],
    [5, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 0, 0, 0, 2, 0],
    [9, 0, 0, 8, 0, 0, 0, 0, 5],
    [0, 5, 0, 0, 0, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0]
]

if solve_puzzle(puzzle):
    for i in range(9):
        for j in range(9):
            print(puzzle[i][j], end=" ")
        print()
else:
    print("No solution exists.")
