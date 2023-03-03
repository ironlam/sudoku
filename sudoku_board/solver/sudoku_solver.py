import numpy as np


def solve_sudoku(board):
    """
    Solves a Sudoku puzzle using backtracking algorithm.

    :param board: numpy 2D array of integers
        A partially filled Sudoku grid.
    :return: numpy 2D array of integers
        A solved Sudoku grid.
    """
    row, col = find_empty_cell(board)

    # If all cells are filled, puzzle is solved
    if row == -1:
        return board

    # Try numbers from 1 to 9
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board) is not None:
                return board
            board[row][col] = 0

    # If no number works, backtrack
    return None


def find_empty_cell(board):
    """
    Finds the next empty cell in the Sudoku board.

    :param board: numpy 2D array of integers
        A partially filled Sudoku grid.
    :return: tuple of integers
        The row and column index of the next empty cell, or (-1, -1) if there is no empty cell.
    """
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                return row, col

    return -1, -1


def is_valid_move(board, row, col, num):
    """
    Checks if a number can be placed in a particular cell of the Sudoku board.

    :param board: numpy 2D array of integers
        A partially filled Sudoku grid.
    :param row: int
        The row index of the cell.
    :param col: int
        The column index of the cell.
    :param num: int
        The number to be placed in the cell.
    :return: bool
        True if the number can be placed in the cell, False otherwise.
    """
    # Check row
    if num in board[row, :]:
        return False

    # Check column
    if num in board[:, col]:
        return False

    # Check box
    box_size = int(np.sqrt(board.shape[0]))
    box_row, box_col = row // box_size, col // box_size
    box = board[box_row * box_size:(box_row + 1) * box_size, box_col * box_size:(box_col + 1) * box_size]
    if num in box:
        return False

    return True
