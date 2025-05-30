import pygame
from Sprites.outlines import Outline, outline_positions
from game.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, OUTLINE_SPACING,
    NORMAL_HIT_ZONE_Y, GRAVITY_HIT_ZONE_Y, HIT_ZONE_EDGE_DISTANCE
)

class OutlineManager:
    def __init__(self, outlines):
        self.outlines = outlines
        self.outline_positions = {}  # Store original positions for reference
        self.key_to_outline_key = {
            'd': 'left_outline',
            'f': 'down_outline',
            'j': 'up_outline',
            'k': 'right_outline'
        }

    def add_outlines(self, outline_group, gravity_mode=False):
        """Add outlines to the group with appropriate positioning."""
        outline_group.empty()  # Clear existing outlines
        
        for key in ['d', 'f', 'j', 'k']:
            outline_key = self.key_to_outline_key[key]
            image = self.outlines[outline_key]
            pos = outline_positions[key]  # This is a tuple (x, y)
            outline = Outline(image, pos[0], key)  # Pass x position directly
            if gravity_mode:
                # Place bottom of outline at HIT_ZONE_EDGE_DISTANCE from top
                outline.rect.y = HIT_ZONE_EDGE_DISTANCE - outline.rect.height
            else:
                # Place top of outline at WINDOW_HEIGHT - HIT_ZONE_EDGE_DISTANCE
                outline.rect.y = WINDOW_HEIGHT - HIT_ZONE_EDGE_DISTANCE
            outline_group.add(outline)
            
            # Store original position for reference
            self.outline_positions[key] = {
                'x': outline.rect.x,
                'y': outline.rect.y
            }

    def update_outline_positions(self, outline_group, gravity_mode):
        """Update outline positions based on gravity mode."""
        for outline in outline_group:
            if gravity_mode:
                outline.rect.y = HIT_ZONE_EDGE_DISTANCE - outline.rect.height
            else:
                outline.rect.y = WINDOW_HEIGHT - HIT_ZONE_EDGE_DISTANCE

class Outline(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, key):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.key = key 