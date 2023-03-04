import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import logging
import pygame
from sudoku import Sudoku

logging.basicConfig(level=logging.DEBUG)


class GUI:
    def __init__(self, size, clues):
        logging.debug('initializing here.')
        self.size = size
        self.clues = clues
        self.sudoku = Sudoku(size)
        self.sudoku.generate(clues)

        try:
            pygame.init()

            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((500, 600))
            pygame.display.set_caption("Sudoku")

            self.font = pygame.font.SysFont("Arial", 36)

            self.new_game_button = Button((10, 520, 150, 50), "New Game")
            self.solve_button = Button((170, 520, 150, 50), "Solve")
            self.reset_button = Button((330, 520, 150, 50), "Reset")

            self.selected_cell = None

            self.run()
        except pygame.error as e:
            logging.error("Pygame initialization error: %s", e)

    def run(self):
        """
        Main game loop.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(60)
            self.handle_events()
            self.draw()
            pygame.display.update()
            pygame.display.flip()

    def handle_events(self):
        """
        Handle events such as mouse clicks and key presses.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.new_game_button.rect.collidepoint(pos):
                    self.new_game()
                elif self.solve_button.rect.collidepoint(pos):
                    self.solve()
                elif self.reset_button.rect.collidepoint(pos):
                    self.reset()
                else:
                    self.selected_cell = self.get_cell_at_pos(pos)
            elif event.type == pygame.KEYDOWN and self.selected_cell is not None:
                if event.unicode.isdigit():
                    self.sudoku.board[self.selected_cell[0]][self.selected_cell[1]] = int(event.unicode)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.sudoku.board[self.selected_cell[0]][self.selected_cell[1]] = 0

    def draw(self):
        """
        Draw the game screen.
        """
        self.screen.fill((255, 255, 255))

        for i in range(self.size):
            for j in range(self.size):
                x = j * 50
                y = i * 50
                rect = pygame.Rect(x, y, 50, 50)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

                if self.sudoku.board[i][j] != 0:
                    text = self.font.render(str(self.sudoku.board[i][j]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

        if self.selected_cell is not None:
            x = self.selected_cell[1] * 50
            y = self.selected_cell[0] * 50
            rect = pygame.Rect(x, y, 50, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)

        self.new_game_button.draw(self.screen)
        self.solve_button.draw(self.screen)
        self.reset_button.draw(self.screen)

        pygame.display.update()
        pygame.display.flip()

    def new_game(self):
        """
        Generate a new Sudoku puzzle.
        """
        self.sudoku.generate(self.clues)
        self.selected_cell = None

    def solve(self):
        """
        Solve the current Sudoku puzzle.
        """
        self.sudoku.solve()
        self.selected_cell = None

    def reset(self):
        """
        Reset the current Sudoku puzzle.
        """
        self.sudoku = Sudoku(self.size)
        self.sudoku.generate(self.clues)
        self.selected_cell = None

    def get_cell_at_pos(self, pos):
        """
        Get the row and column of the cell at the given position.
        """
        x, y = pos
        row = y // 50
        col = x // 50
        if row < self.size and col < self.size:
            return row, col
        else:
            return None


class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = pygame.font.SysFont("Arial", 24)
        pygame.display.set_caption("Sudoku")

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)