import random
import numpy as np
from .solver.sudoku_solver import solve_sudoku, find_empty_cell


class SudokuBoard:
    def __init__(self, size=9):
        self.givens = None
        self.copy_grid = None
        self.grid = None
        self.size = size
        self.reset()

    def reset(self):
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.create_board()
        self.givens = np.copy(self.grid)
        self.copy_grid = np.copy(self.grid)

    def create_board(self):
        self.grid = solve_sudoku(np.zeros((self.size, self.size), dtype=int))
        self.remove_values()

    def remove_values(self):
        for i in range(self.size):
            for j in range(self.size):
                if random.random() <= 0.6:
                    self.grid[i][j] = 0

    def is_given(self, row, col):
        return self.givens[row][col] != 0

    def is_complete(self):
        return (self.grid != 0).all() and self.is_valid()

    def is_valid(self):
        for i in range(self.size):
            if not self.is_valid_row(i) or not self.is_valid_column(i) or not self.is_valid_square(i):
                return False
        return True

    def is_valid_row(self, row):
        return len(set(self.grid[row, :])) == self.size

    def is_valid_column(self, col):
        return len(set(self.grid[:, col])) == self.size

    def is_valid_square(self, square):
        row_start = (square // int(np.sqrt(self.size))) * int(np.sqrt(self.size))
        col_start = (square % int(np.sqrt(self.size))) * int(np.sqrt(self.size))
        square_values = self.grid[row_start:row_start + int(np.sqrt(self.size)), col_start:col_start + int(np.sqrt(self.size))].ravel()
        return len(set(square_values)) == self.size

    def set_value(self, row, col, value):
        self.grid[row][col] = value

    def get_value(self, row, col):
        return self.grid[row][col]

    def copy(self):
        new_board = SudokuBoard(self.size)
        new_board.grid = np.copy(self.grid)
        new_board.givens = np.copy(self.givens)
        new_board.copy_grid = np.copy(self.copy_grid)
        return new_board

    def solve(self):
        self.grid = solve_sudoku(self.grid)

    def get_empty_cells(self):
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    def is_valid_value(self, row, col, value):
        # Check if the value is already in the same row or column
        if value in self.grid[row, :] or value in self.grid[:, col]:
            return False

        # Check if the value is already in the same square
        row_start = (row // int(np.sqrt(self.size))) * int(np.sqrt(self.size))
        col_start = (col // int(np.sqrt(self.size))) * int(np.sqrt(self.size))
        square_values = self.grid[row_start:row_start + int(np.sqrt(self.size)), col_start:col_start + int(np.sqrt(self.size))]
        if value in square_values:
            return False

        return True
