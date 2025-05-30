import pygame
from game.constants import WINDOW_HEIGHT


class Tiles(pygame.sprite.Sprite):
    def __init__(self, image, pos, key):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.key = key  # Store the key for hit detection
        
        # Create a hitbox that's slightly smaller than the arrow sprite
        hitbox_width = self.rect.width * 0.8  # 80% of sprite width
        hitbox_height = self.rect.height * 0.8  # 80% of sprite height
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center

    def update(self, speed):
        self.rect.y += speed
        self.hitbox.center = self.rect.center  # Update hitbox position with arrow
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()


spawn_positions = {
    'd': (270, -100),  # Start off-screen
    'f': (540, -100),
    'j': (810, -100),
    'k': (1080, -100)
}
