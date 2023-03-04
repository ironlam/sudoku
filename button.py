import pygame
from constants import *
from text import Text


class Button:
    def __init__(self, pos, size, text):
        self.rect = pygame.Rect(pos, size)
        self.text = Text(self.rect.center, text)

    def clicked(self):
        # Return True if the button was clicked
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def handle_event(self, event):
        # Change the button color when the mouse is over it
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.text.color = BUTTON_HOVER_COLOR
            else:
                self.text.color = BUTTON_COLOR

    def draw(self, screen):
        # Draw the button
        pygame.draw.rect(screen, self.text.color, self.rect)
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, self.rect, 2)
        self.text.draw(screen)
