def solve_sudoku(board):
    # Find the first empty cell
    row, col = find_empty_cell(board)

    # If there are no empty cells, the board is solved
    if row is None:
        return True

    # Try all possible values for the cell
    for value in range(1, board.size + 1):
        if board.is_valid_value(row, col, value):
            board.set_value(row, col, value)

            # Recursively try to solve the rest of the board
            if solve_sudoku(board):
                return True

            # If the board is not solvable with the current value, backtrack
            board.set_value(row, col, 0)

    # If no values work, the puzzle is unsolvable
    return False


def find_empty_cell(board):
    for row in range(board.size):
        for col in range(board.size):
            if board.get_value(row, col) == 0:
                return row, col
    return None, None
