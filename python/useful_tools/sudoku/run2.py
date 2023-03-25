"""


Created at 2023/2/27
"""


def solve_sudoku(board):
    """
    Solve the given Sudoku board using recursive backtracking algorithm.

    Args:
        board: list[list[int]]
            A 9x9 Sudoku board with 0 representing empty cells.

    Returns:
        bool:
            True if a solution is found, False otherwise.
    """
    # Find an empty cell on the board
    row, col = find_empty_cell(board)
    if row == -1 and col == -1:
        # All cells are filled, solution is found
        return True

    # Try to fill the empty cell with numbers 1 to 9
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            # If solution is not found, backtrack and try the next number
            board[row][col] = 0

    # All numbers are tried and no solution is found
    return False


def find_empty_cell(board):
    """
    Find an empty cell on the board.

    Args:
        board: list[list[int]]
            A 9x9 Sudoku board with 0 representing empty cells.

    Returns:
        tuple[int, int]:
            The row and column indices of an empty cell, or (-1, -1) if there is no empty cell.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return -1, -1


def is_valid_move(board, row, col, num):
    """
    Check if filling the given number in the given cell is a valid move.

    Args:
        board: list[list[int]]
            A 9x9 Sudoku board with 0 representing empty cells.
        row: int
            The row index of the cell.
        col: int
            The column index of the cell.
        num: int
            The number to be filled in the cell.

    Returns:
        bool:
            True if the move is valid, False otherwise.
    """
    # Check the row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check the 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False

    # The move is valid
    return True
