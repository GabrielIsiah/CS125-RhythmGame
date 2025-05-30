import pygame
import os

class FontManager:
    def __init__(self):
        self.fonts = {}
        self.font_path = os.path.join('assets', 'fonts', 'Grand9k Pixel.ttf')
        
    def get_font(self, size):
        """Get a font object with the specified size."""
        if size not in self.fonts:
            try:
                self.fonts[size] = pygame.font.Font(self.font_path, size)
            except pygame.error:
                print(f"Warning: Could not load font from {self.font_path}. Using system font.")
                self.fonts[size] = pygame.font.SysFont("arial", size)
            except Exception as e:
                print(f"An unexpected error occurred loading font: {e}. Using system font.")
                self.fonts[size] = pygame.font.SysFont("arial", size)
        return self.fonts[size]

# Create a global font manager instance
font_manager = FontManager() 