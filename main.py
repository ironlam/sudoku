import pygame
from board import Board
from button import Button
from constants import *

# Initialize Pygame
pygame.init()

# Set the window size and title
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku")

# Create the buttons
solve_button = Button(SOLVE_BUTTON_POS, SOLVE_BUTTON_SIZE, "Solve")
new_board_button = Button(NEW_BOARD_BUTTON_POS, NEW_BOARD_BUTTON_SIZE, "New Board")
reset_button = Button(RESET_BUTTON_POS, RESET_BUTTON_SIZE, "Reset")

# Initialize the board
board = Board()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any button was clicked
            if solve_button.clicked():
                board.solve()
            elif new_board_button.clicked():
                board.new_board()
            elif reset_button.clicked():
                board.reset()

        # Update the board and buttons
        board.handle_event(event)
        solve_button.handle_event(event)
        new_board_button.handle_event(event)
        reset_button.handle_event(event)

    # Draw the board and buttons
    screen.fill(BACKGROUND_COLOR)
    board.draw(screen)
    solve_button.draw(screen)
    new_board_button.draw(screen)
    reset_button.draw(screen)

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
