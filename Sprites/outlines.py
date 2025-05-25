import pygame


class Outline(pygame.sprite.Sprite):
    def __init__(self, image, pos, key):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.key = key


outline_positions = {
    'd': (270, 750),
    'f': (540, 750),
    'j': (810, 750),
    'k': (1080, 750),
}

