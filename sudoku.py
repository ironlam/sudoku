import random


class Sudoku:
    def __init__(self, board_size):
        self.board_size = board_size
        self.grid_size = int(board_size ** 0.5)
        self.board = [[0 for i in range(board_size)] for j in range(board_size)]
        self.generate_board()

    def generate_board(self):
        self.fill_diagonal_blocks()
        self.fill_remaining(0, self.grid_size)
        self.remove_cells()

    def fill_diagonal_blocks(self):
        for i in range(0, self.board_size, self.grid_size):
            self.fill_block(i, i)

    def fill_block(self, row, col):
        block = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                num = random.randint(1, self.board_size)
                while num in block:
                    num = random.randint(1, self.board_size)
                block.append(num)
                self.board[row + i][col + j] = num

    def fill_remaining(self, row, col):
        if col >= self.board_size and row < self.board_size - 1:
            row += 1
            col = 0
        if row >= self.board_size and col >= self.board_size:
            return True
        if row < self.grid_size:
            if col < self.grid_size:
                col = self.grid_size
        elif row < self.board_size - self.grid_size:
            if col == int(row / self.grid_size) * self.grid_size:
                col += self.grid_size
        else:
            if col == self.board_size - self.grid_size:
                row += 1
                col = 0
                if row >= self.board_size:
                    return True
        for num in range(1, self.board_size + 1):
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def is_safe(self, row, col, num):
        for i in range(self.board_size):
            if self.board[row][i] == num:
                return False
        for i in range(self.board_size):
            if self.board[i][col] == num:
                return False
        row_start = (row // self.grid_size) * self.grid_size
        col_start = (col // self.grid_size) * self.grid_size
        for i in range(row_start, row_start + self.grid_size):
            for j in range(col_start, col_start + self.grid_size):
                if self.board[i][j] == num:
                    return False
        return True

    def remove_cells(self):
        clues = self.get_num_clues()
        cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size)]
        random.shuffle(cells)
        for i, j in cells:
            temp = self.board[i][j]
            self.board[i][j] = 0
            if not self.is_unique_solution():
                self.board[i][j] = temp
            clues -= 1
            if clues == 0:
                return

    def get_num_clues(self):
        if self.board_size == 9:
            return 17
        elif self.board_size == 4:
            return 5
        elif self.board_size == 6:
            return 12

    def is_unique_solution(self):
        solution = [[self.board[i][j] for j in range(self.board_size)] for i in range(self.board_size)]
        return self.solve(solution)

    def solve(self, board):
        row, col, unassigned = self.find_unassigned(board)
        if unassigned == 0:
            return True
        for num in range(1, self.board_size + 1):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0
        return False

    def find_unassigned(self, board):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 0:
                    return i, j, 1
        return -1, -1, 0

    def is_valid(self, board, row, col, num):
        for i in range(self.board_size):
            if board[row][i] == num:
                return False
        for i in range(self.board_size):
            if board[i][col] == num:
                return False
        row_start = (row // self.grid_size) * self.grid_size
        col_start = (col // self.grid_size) * self.grid_size
        for i in range(row_start, row_start + self.grid_size):
            for j in range(col_start, col_start + self.grid_size):
                if board[i][j] == num:
                    return False
        return True


