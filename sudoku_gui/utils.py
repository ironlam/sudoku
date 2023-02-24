import os
import pygame


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)


def load_image(name, colorkey=None):
    fullname = os.path.join('sudoku_gui', 'images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as e:
        print(f'Cannot load image: {fullname}')
        raise SystemExit(str(e))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


def draw_text(surface, text, font, color, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.centerx = x
        text_rect.centery = y
    else:
        text_rect.x = x
        text_rect.y = y
    surface.blit(text_obj, text_rect)
