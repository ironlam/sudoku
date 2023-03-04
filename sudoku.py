import random


class Sudoku:
    def __init__(self, size):
        self.size = size
        self.board = None

    def generate(self, clues):
        """
        Generate a new Sudoku puzzle with the given number of clues.
        """
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

        # Fill in a random diagonal pattern of digits
        digits = list(range(1, self.size + 1))
        random.shuffle(digits)
        for i in range(0, self.size, int(self.size ** 0.5)):
            for j in range(int(self.size ** 0.5)):
                self.board[i + j][i + j] = digits.pop()

        # Solve the incomplete puzzle
        self.solve()

        # Remove a random set of clues to create the puzzle
        coords = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(coords)
        for i, j in coords:
            temp = self.board[i][j]
            self.board[i][j] = 0
            if not self.has_unique_solution(clues):
                self.board[i][j] = temp

    def has_unique_solution(self, max_solutions=1):
        """
        Check if the current Sudoku puzzle has a unique solution.
        """
        solutions = []
        self.solve(solutions)
        return len(solutions) == max_solutions

    def solve(self, solutions=None):
        """
        Solve the current Sudoku puzzle using backtracking.
        """
        if solutions is None:
            solutions = []

        # Find the first empty cell
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    break
            else:
                continue
            break
        else:
            solutions.append([row[:] for row in self.board])
            return

        # Try all possible digits in the empty cell
        for digit in range(1, self.size + 1):
            if self.is_valid(i, j, digit):
                self.board[i][j] = digit
                self.solve(solutions)
                self.board[i][j] = 0

    def is_valid(self, row, col, digit):
        """
        Check if the given digit can be placed in the given cell.
        """
        # Check row and column for duplicates
        for i in range(self.size):
            if self.board[row][i] == digit or self.board[i][col] == digit:
                return False

        # Check block for duplicates
        block_size = int(self.size ** 0.5)
        block_row = (row // block_size) * block_size
        block_col = (col // block_size) * block_size
        for i in range(block_row, block_row + block_size):
            for j in range(block_col, block_col + block_size):
                if self.board[i][j] == digit:
                    return False

        return True
