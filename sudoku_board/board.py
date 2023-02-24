import numpy as np
import sys

sys.path.append('../sudoku_board/solver')

from .solver import solve_sudoku


class SudokuBoard:
    def __init__(self, size=9):
        self.size = size
        self.box_size = int(np.sqrt(size))
        self.grid = np.zeros((size, size), dtype=int)

    def set_value(self, row, col, value):
        if 1 <= value <= self.size:
            self.grid[row][col] = value

    def get_value(self, row, col):
        return self.grid[row][col]

    def is_valid_value(self, row, col, value):
        if value == 0:
            return True

        # Check if value appears in the row
        if value in self.grid[row]:
            return False

        # Check if value appears in the column
        if value in [self.grid[i][col] for i in range(self.size)]:
            return False

        # Check if value appears in the box
        box_row = (row // self.box_size) * self.box_size
        box_col = (col // self.box_size) * self.box_size
        for i in range(box_row, box_row + self.box_size):
            for j in range(box_col, box_col + self.box_size):
                if self.grid[i][j] == value:
                    return False

        return True

    def is_complete(self):
        return not (self.grid == 0).any()

    def reset(self):
        self.grid = np.zeros((self.size, self.size), dtype=int)

    def solve(self):
        self.grid = solve_sudoku(self.grid)
