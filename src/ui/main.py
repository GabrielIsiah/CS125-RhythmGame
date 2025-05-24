import pygame
import sys
import os
from ..components.button import Button

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

# UI Constants
COLORS = {
    "GOLD": "#b68f40",
    "GREEN": "#d7fcd4",
    "WHITE": "White",
    "BLACK": "black",
    "HOVER_GREEN": "#a0f5b0", # A slightly different green for hover effect if needed
    "RED": "red" # Added Red color
}

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
BG_PATH = os.path.join(ASSET_DIR, "background.png")
FONT_PATH = os.path.join(ASSET_DIR, "Grand9k Pixel.ttf") # Updated to use the correct font filename

# Load assets
try:
    BG = pygame.image.load(BG_PATH).convert()
except pygame.error:
    print(f"Warning: Could not load background image from {BG_PATH}. Using black background.")
    BG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    BG.fill(COLORS["BLACK"])
except Exception as e: # Catch other exceptions as well
    print(f"An unexpected error occurred loading background image: {e}. Using black background.")
    BG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    BG.fill(COLORS["BLACK"])

def get_font(size):
    """Get a font object with the specified size."""
    # Replace 'None' with FONT_PATH if you add a pixel font file
    try:
        return pygame.font.Font(FONT_PATH, size) # Use this line if you have a pixel font file
        # return pygame.font.Font(None, size)  # Using default font if no file specified
    except pygame.error:
        print(f"Warning: Could not load font from {FONT_PATH}. Using system font.") # Simplified error message
        return pygame.font.SysFont("arial", size)  # Fallback to system font
    except Exception as e: # Catch other exceptions as well
        print(f"An unexpected error occurred loading font: {e}. Using system font.")
        return pygame.font.SysFont("arial", size) # Fallback to system font for other errors

def play():
    """Play game screen."""
    pygame.display.set_caption("Play")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])
        
        # Game title
        play_text = get_font(100).render("PLAY", True, COLORS["GOLD"])
        play_rect = play_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        SCREEN.blit(play_text, play_rect)
        
        # Back button
        back_button = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 400),
            text_input="BACK",
            font=get_font(75),
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        )

        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    main_menu()
        
        pygame.display.update()

def endless():
    """Endless mode screen."""
    pygame.display.set_caption("Endless")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])
        
        # Mode title
        endless_text = get_font(100).render("ENDLESS", True, COLORS["GOLD"])
        endless_rect = endless_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        SCREEN.blit(endless_text, endless_rect)
        
        # Back button
        back_button = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 400),
            text_input="BACK",
            font=get_font(75),
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        )

        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    main_menu()
        
        pygame.display.update()

def main_menu():
    """Main menu screen."""
    pygame.display.set_caption("MPEPE")
    
    while True:
        SCREEN.blit(BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        
        # Menu title
        menu_text = get_font(100).render("MPEPE", True, COLORS["GOLD"])
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(menu_text, menu_rect)
        
        # Menu buttons
        buttons = [
            Button(
                image=None,
                pos=(SCREEN_WIDTH//2, 250),
                text_input="PLAY",
                font=get_font(75),
                base_color=COLORS["WHITE"],
                hovering_color=COLORS["RED"]
            ),
            Button(
                image=None,
                pos=(SCREEN_WIDTH//2, 400),
                text_input="ENDLESS",
                font=get_font(75),
                base_color=COLORS["WHITE"],
                hovering_color=COLORS["RED"]
            ),
            Button(
                image=None,
                pos=(SCREEN_WIDTH//2, 550),
                text_input="QUIT",
                font=get_font(75),
                base_color=COLORS["WHITE"],
                hovering_color=COLORS["RED"]
            )
        ]

        # Update buttons
        for button in buttons:
            button.changeColor(mouse_pos)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].checkForInput(mouse_pos):  # Play button
                    play()
                if buttons[1].checkForInput(mouse_pos):  # Endless button
                    endless()
                if buttons[2].checkForInput(mouse_pos): # Quit button
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
