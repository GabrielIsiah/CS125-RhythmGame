import pygame
import sys
import os
from Utility.font_manager import font_manager
from game.game import Game
from assets import outlines, arrows

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# UI Constants
COLORS = {
    "GOLD": "#b68f40",
    "GREEN": "#d7fcd4",
    "WHITE": "White",
    "BLACK": "black",
    "HOVER_GREEN": "#a0f5b0", 
    "RED": "red" 
}

# Song data
SONGS = {
    "song1": {
        "title": "Default Song",
        "artist": "Unknown Artist",
        "difficulty": {
            "easy": {"file": "key_log.csv", "bpm": 120},
            "medium": {"file": "key_log.csv", "bpm": 140},
            "hard": {"file": "key_log.csv", "bpm": 160}
        }
    }
    # Add more songs here
}

class Button:
    def __init__(self, image, pos, text_input, font_size, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font_manager.get_font(font_size)
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.is_hovering = False

        if self.image is None:
            text_surface = self.font.render(self.text_input, True, self.base_color)
            self.image = pygame.Surface((text_surface.get_width() + 40, text_surface.get_height() + 20), pygame.SRCALPHA)
            self.image.blit(text_surface, (20, 10))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            if not self.is_hovering:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
                self.is_hovering = True
        else:
            if self.is_hovering:
                self.text = self.font.render(self.text_input, True, self.base_color)
                self.is_hovering = False

def start_game(song_key, difficulty):
    """Start the rhythm game with selected song and difficulty."""
    game = Game(outlines, arrows, song_key, difficulty)
    game.run()
    # After game ends, return to song selection
    song_selection()
    return

def song_selection():
    """Song selection screen."""
    pygame.display.set_caption("Select Song")
    
    # Create difficulty buttons
    difficulty_buttons = [
        Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 400),
            text_input="EASY",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        ),
        Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 500),
            text_input="MEDIUM",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        ),
        Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 600),
            text_input="HARD",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        )
    ]
    
    # Back button
    back_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2, 700),
        text_input="BACK",
        font_size=75,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"]
    )
    
    selected_song = "song1"  # Default to first song
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])
        
        # Draw title
        title_text = font_manager.get_font(100).render("SELECT DIFFICULTY", True, COLORS["GOLD"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(title_text, title_rect)
        
        # Draw song info
        song = SONGS[selected_song]
        song_text = font_manager.get_font(50).render(f"{song['title']} - {song['artist']}", True, COLORS["WHITE"])
        song_rect = song_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        SCREEN.blit(song_text, song_rect)
        
        # Update and draw difficulty buttons
        for button in difficulty_buttons:
            button.changeColor(mouse_pos)
            button.update(SCREEN)
        
        # Update and draw back button
        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if difficulty_buttons[0].checkForInput(mouse_pos):  # Easy
                    start_game(selected_song, "easy")
                    return
                if difficulty_buttons[1].checkForInput(mouse_pos):  # Medium
                    start_game(selected_song, "medium")
                    return
                if difficulty_buttons[2].checkForInput(mouse_pos):  # Hard
                    start_game(selected_song, "hard")
                    return
                if back_button.checkForInput(mouse_pos):
                    play()
                    return
        
        pygame.display.update()

def play():
    """Play game screen."""
    pygame.display.set_caption("Play")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])
        
        # Game title
        play_text = font_manager.get_font(100).render("PLAY", True, COLORS["GOLD"])
        play_rect = play_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        SCREEN.blit(play_text, play_rect)
        
        # Difficulty button (was Pattern Mode)
        difficulty_button = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 400),
            text_input="DIFFICULTY",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        )
        
        # Back button
        back_button = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 500),
            text_input="BACK",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        )

        difficulty_button.changeColor(mouse_pos)
        difficulty_button.update(SCREEN)
        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if difficulty_button.checkForInput(mouse_pos):
                    pattern_selection()
                    return
                if back_button.checkForInput(mouse_pos):
                    main_menu()
                    return
        
        pygame.display.update()

def pattern_selection():
    """Difficulty selection screen (was Pattern Mode)."""
    pygame.display.set_caption("Difficulty")
    
    # Create difficulty buttons
    difficulty_buttons = [
        Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 400),
            text_input="EASY",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        ),
        Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 500),
            text_input="MEDIUM",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        ),
        Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 600),
            text_input="HARD",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"]
        )
    ]
    
    # Back button
    back_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2, 700),
        text_input="BACK",
        font_size=75,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"]
    )
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])
        
        # Draw title
        title_text = font_manager.get_font(100).render("DIFFICULTY", True, COLORS["GOLD"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = font_manager.get_font(50).render("Select Difficulty", True, COLORS["WHITE"])
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        SCREEN.blit(subtitle_text, subtitle_rect)
        
        # Update and draw difficulty buttons
        for button in difficulty_buttons:
            button.changeColor(mouse_pos)
            button.update(SCREEN)
        
        # Update and draw back button
        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if difficulty_buttons[0].checkForInput(mouse_pos):  # Easy
                    pattern_ready_screen("easy")
                    return
                if difficulty_buttons[1].checkForInput(mouse_pos):  # Medium
                    pattern_ready_screen("medium")
                    return
                if difficulty_buttons[2].checkForInput(mouse_pos):  # Hard
                    pattern_ready_screen("hard")
                    return
                if back_button.checkForInput(mouse_pos):
                    play()
                    return
        
        pygame.display.update()

def pattern_ready_screen(selected_pattern_difficulty):
    """Difficulty ready screen with PLAY and BACK (was Pattern Mode Ready)."""
    pygame.display.set_caption("Difficulty Ready")
    
    # Play and Back buttons
    play_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2, 500),
        text_input="PLAY",
        font_size=75,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"]
    )
    back_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2, 600),
        text_input="BACK",
        font_size=75,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"]
    )
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])
        
        # Draw title
        title_text = font_manager.get_font(100).render("(SONG TITLE)", True, COLORS["GOLD"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(title_text, title_rect)
        
        # Draw selected difficulty
        diff_text = font_manager.get_font(60).render(f"Selected Difficulty: {selected_pattern_difficulty.upper()}", True, COLORS["WHITE"])
        diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        SCREEN.blit(diff_text, diff_rect)
        
        # Update and draw buttons
        play_button.changeColor(mouse_pos)
        play_button.update(SCREEN)
        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_pos):
                    start_game("pattern", selected_pattern_difficulty)
                    return
                if back_button.checkForInput(mouse_pos):
                    pattern_selection()
                    return
        
        pygame.display.update()

def endless():
    """Endless mode screen."""
    pygame.display.set_caption("Endless")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])
        
        # Mode title
        endless_text = font_manager.get_font(100).render("ENDLESS", True, COLORS["GOLD"])
        endless_rect = endless_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        SCREEN.blit(endless_text, endless_rect)
        
        # Back button
        back_button = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 400),
            text_input="BACK",
            font_size=75,
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
    pygame.display.set_caption("Rhythm Game")
    
    while True:
        SCREEN.fill(COLORS["BLACK"])
        mouse_pos = pygame.mouse.get_pos()
        
        # Menu title
        menu_text = font_manager.get_font(100).render("RHYTHM GAME", True, COLORS["GOLD"])
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(menu_text, menu_rect)
        
        # Menu buttons
        buttons = [
            Button(
                image=None,
                pos=(SCREEN_WIDTH//2, 250),
                text_input="PLAY",
                font_size=75,
                base_color=COLORS["WHITE"],
                hovering_color=COLORS["RED"]
            ),
            Button(
                image=None,
                pos=(SCREEN_WIDTH//2, 400),
                text_input="ENDLESS",
                font_size=75,
                base_color=COLORS["WHITE"],
                hovering_color=COLORS["RED"]
            ),
            Button(
                image=None,
                pos=(SCREEN_WIDTH//2, 550),
                text_input="QUIT",
                font_size=75,
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
                if buttons[2].checkForInput(mouse_pos):  # Quit button
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update() 