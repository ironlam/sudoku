import pygame
import random
from constants import *
from text import Text


class Board:
    def __init__(self, size=9):
        self.size = size
        self.block_size = int(CELL_SIZE * self.size ** 0.5)
        self.cells = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.clues = 0
        self.selected = None
        self.font = pygame.font.Font(None, int(CELL_SIZE * 0.8))

        # Generate a new board
        self.new_board()

    def new_board(self):
        # Clear the board
        self.cells = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.selected = None

        # Generate pre-filled cells
        if self.size == 4:
            self.clues = 5
        elif self.size == 6:
            self.clues = 12
        else:
            self.clues = 17

        for i in range(self.clues):
            while True:
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
                if self.cells[row][col] == 0:
                    self.cells[row][col] = random.randint(1, self.size)
                    break

    def reset(self):
        # Clear the board and re-fill it with clues
        self.cells = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.selected = None
        self.new_board()

    def solve(self):
        # Solve the board using backtracking
        if self._solve():
            print("Sudoku solved!")
        else:
            print("Cannot solve Sudoku puzzle.")

    def _solve(self):
        # Find the next empty cell
        empty_cell = self._find_empty_cell()
        if not empty_cell:
            return True

        row, col = empty_cell

        # Try each possible value for the empty cell
        for num in range(1, self.size + 1):
            if self._is_valid(num, row, col):
                self.cells[row][col] = num

                # Recursively solve the remaining cells
                if self._solve():
                    return True

                # Undo the cell if the solution is not valid
                self.cells[row][col] = 0

        # If no value works, backtrack
        return False

    def _find_empty_cell(self):
        # Find the next empty cell
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    return (i, j)
        return None

    def _is_valid(self, num, row, col):
        # Check if the number is valid for the row
        for i in range(self.size):
            if self.cells[row][i] == num:
                return False

        # Check if the number is valid for the column
        for j in range(self.size):
            if self.cells[j][col] == num:
                return False

        # Check if the number is valid for the block
        block_row = (row // int(self.size ** 0.5)) * int(self.size ** 0.5)
        block_col = (col // int(self.size ** 0.5)) * int(self.size ** 0.5)
        for i in range(int(self.size ** 0.5)):
            for j in range(int(self.size ** 0.5)):
                if self.cells[block_row + i][block_col + j] == num:
                    return False

        # If the number is valid for the row, column, and block, return True
        return True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the cell that was clicked
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // CELL_SIZE
            col = mouse_pos[0] // CELL_SIZE
            if row < self.size and col < self.size:
                self.selected = (row, col)

        elif event.type == pygame.KEYDOWN:
            if self.selected:
                # Set the cell value if it is valid
                if event.unicode.isdigit() and int(event.unicode) in range(1, self.size + 1):
                    self.cells[self.selected[0]][self.selected[1]] = int(event.unicode)
                    self.selected = None

                # Clear the cell if the backspace key was pressed
                elif event.key == pygame.K_BACKSPACE:
                    self.cells[self.selected[0]][self.selected[1]] = 0

    def draw(self, screen):
        # Draw the background
        screen.fill(BACKGROUND_COLOR)

        # Draw the grid
        for i in range(self.size):
            for j in range(self.size):
                rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, CELL_COLOR, rect, 1)

                # Draw the cell value
                if self.cells[i][j] != 0:
                    text = self.font.render(str(self.cells[i][j]), True, CELL_TEXT_COLOR)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        # Draw the selected cell
        if self.selected:
            rect = pygame.Rect(self.selected[1] * CELL_SIZE, self.selected[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, SELECTED_CELL_COLOR, rect, 1)

        # Draw the block borders
        for i in range(int(self.size ** 0.5)):
            for j in range(int(self.size ** 0.5)):
                rect = pygame.Rect(j * self.block_size, i * self.block_size, self.block_size, self.block_size)
                pygame.draw.rect(screen, BLOCK_COLOR, rect, 3)

