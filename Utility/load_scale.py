import pygame


def load_scale(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


def rotate_img(image, angle):
    return pygame.transform.rotate(image, angle)
