import pygame
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize pygame and set video mode
pygame.init()
pygame.display.init()
pygame.display.set_mode((1600, 900))  # Set video mode before loading assets

from game.game import Game
from assets import outlines, arrows

if __name__ == "__main__":
    game = Game(outlines, arrows)
    game.run()
