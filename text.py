import pygame
from constants import *


class Text:
    def __init__(self, pos, text, color=BUTTON_COLOR):
        self.pos = pos
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Arial", 12)

    def draw(self, screen):
        # Draw the text
        text = self.font.render(self.text, True, self.color)
        rect = text.get_rect(center=self.pos)
        screen.blit(text, rect)
