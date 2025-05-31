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
        "title": "Realize (Re:Zero Opening 2)",
        "artist": "Konomi Suzuki",
        "music_file": "assets/songs/Song 1/audio/song.mp3",
        "key_log_file": "assets/songs/Song 1/key_log.csv",
        "difficulty": {
            "easy": {"bpm": 120},
            "medium": {"bpm": 140},
            "hard": {"bpm": 160}
        }
    },
    "song2": {
        "title": "Untitled Song 2",
        "artist": "Unknown Artist",
        "music_file": "assets/songs/Song 1/audio/song2.mp3", # Placeholder for Song 2 music file
        "key_log_file": "", # Placeholder for Song 2 key log file
        "difficulty": {
            "easy": {"bpm": 120},
            "medium": {"bpm": 140},
            "hard": {"bpm": 160}
        }
    },
    "song3": {
        "title": "Untitled Song 3",
        "artist": "Unknown Artist",
        "music_file": "", # Placeholder for Song 3 music file
        "key_log_file": "", # Placeholder for Song 3 key log file
        "difficulty": {
            "easy": {"bpm": 120},
            "medium": {"bpm": 140},
            "hard": {"bpm": 160}
        }
    }
    # Add more songs here
}

class Button:
    def __init__(self, image, pos, text_input, font_size, base_color, hovering_color, width=None, height=None):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font_manager.get_font(font_size)
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.is_hovering = False
        self.width = width
        self.height = height

        # Define standard button dimensions if none are provided
        standard_width = 350
        standard_height = 90

        # Use fixed width and height if provided, otherwise use standard, otherwise calculate with padding
        if self.width is not None and self.height is not None:
            button_width = self.width
            button_height = self.height
        elif image is None: # Apply standard size only if no image is used
             button_width = standard_width
             button_height = standard_height
        else:
            # Define padding around the text
            padding_x = 30
            padding_y = 20
            # Calculate size based on potentially multiple lines of text
            lines = self.text_input.split('\n')
            max_width = 0
            total_height = 0
            for line in lines:
                line_surface = self.font.render(line, True, self.base_color)
                max_width = max(max_width, line_surface.get_width())
                total_height += line_surface.get_height()

            button_width = max_width + 2 * padding_x
            button_height = total_height + 2 * padding_y
            
        if self.image is None:
            # Calculate size based on potentially multiple lines of text if not already done
            if self.width is None and self.height is None:
                 lines = self.text_input.split('\n')
                 max_width = 0
                 total_height = 0
                 for line in lines:
                     line_surface = self.font.render(line, True, self.base_color)
                     max_width = max(max_width, line_surface.get_width())
                     total_height += line_surface.get_height()

                 button_width = max_width + 2 * padding_x
                 button_height = total_height + 2 * padding_y

            self.image = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
            
            # Draw the button shape (a simple rounded rectangle for a start)
            button_color = (50, 50, 50, 180) # Dark gray with some transparency
            border_color = (200, 200, 200) # Light gray border
            border_width = 3
            border_radius = 10
            
            # Draw the filled rectangle
            pygame.draw.rect(self.image, button_color, (0, 0, button_width, button_height), border_radius=border_radius)
            # Draw the border
            pygame.draw.rect(self.image, border_color, (0, 0, button_width, button_height), border_width, border_radius=border_radius)

            # Blit the text onto the button image (handle multiple lines)
            lines = self.text_input.split('\n')
            current_y = (button_height - sum(self.font.render(line, True, self.base_color).get_height() for line in lines)) // 2
            for line in lines:
                line_surface = self.font.render(line, True, self.base_color)
                line_rect = line_surface.get_rect(center=(button_width // 2, current_y + line_surface.get_height() // 2))
                self.image.blit(line_surface, line_rect)
                current_y += line_surface.get_height()

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        # We don't need a separate text_rect anymore as text is part of the image
        # self.text_rect = self.text.get_rect(center=self.rect.center) # Keep for consistency if needed elsewhere, but text is drawn on image

    # The update method remains the same as it blits the button's surface (self.image)
    def update(self, screen):
        screen.blit(self.image, self.rect)
        # No need to blit self.text separately anymore
        # screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    # Modify changeColor to update the appearance of the drawn button
    def changeColor(self, position):
        is_now_hovering = position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)

        if is_now_hovering != self.is_hovering:
            self.is_hovering = is_now_hovering
            # Re-render the button image with the appropriate text color
            text_color = self.hovering_color if self.is_hovering else self.base_color

            # Redraw the button background and border using potentially fixed size
            button_width, button_height = self.image.get_size()

            self.image = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
            
            button_color = (50, 50, 50, 180) # Dark gray with some transparency
            border_color = (255, 0, 0) if self.is_hovering else (200, 200, 200) # Red border on hover, light gray otherwise
            border_width = 3
            border_radius = 10

            pygame.draw.rect(self.image, button_color, (0, 0, button_width, button_height), border_radius=border_radius)
            pygame.draw.rect(self.image, border_color, (0, 0, button_width, button_height), border_width, border_radius=border_radius)

            # Blit the text onto the button image (handle multiple lines)
            lines = self.text_input.split('\n')
            current_y = (button_height - sum(self.font.render(line, True, self.base_color).get_height() for line in lines)) // 2
            for line in lines:
                line_surface = self.font.render(line, True, text_color)
                line_rect = line_surface.get_rect(center=(button_width // 2, current_y + line_surface.get_height() // 2))
                self.image.blit(line_surface, line_rect)
                current_y += line_surface.get_height()

    # Keep the original changeColor logic as a reference if needed
    # def changeColor(self, position):
    #     if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
    #         if not self.is_hovering:
    #             self.text = self.font.render(self.text_input, True, self.hovering_color)
    #             self.is_hovering = True
    #     else:
    #         if self.is_hovering:
    #             self.text = self.font.render(self.text_input, True, self.base_color)
    #             self.is_hovering = False

def start_game(song_key, difficulty, mode="normal"):
    """Start the rhythm game with selected song, difficulty, and mode."""
    # Initialize pygame mixer if not already initialized
    if not pygame.mixer.get_init():
        pygame.mixer.init()
        
    game = Game(outlines, arrows, SONGS, song_key, difficulty, mode)
    next_action = game.run()
    
    # Clean up resources before any navigation
    game.cleanup()
    
    # After game ends, navigate based on the returned action
    if mode == "normal":
        if next_action == 'restart':
            # Small delay to ensure resources are properly cleaned up
            pygame.time.wait(100)
            start_game(song_key, difficulty, mode) # Restart the same game
        elif next_action == 'difficulty_select':
            pattern_selection(song_key) # Go back to difficulty selection for the same song
        else: # Covers 'quit' or None (window close)
            main_menu() # Go back to the main menu
    elif mode == "endless":
        if next_action == 'restart_endless':
            # Small delay to ensure resources are properly cleaned up
            pygame.time.wait(100)
            start_game(song_key, difficulty, mode) # Restart endless mode with same song
        else: # Covers 'quit' or None (window close)
            main_menu() # Go back to the main menu
    
    # The return in the menu functions will handle actually returning to the game loop
    # return # No longer needed as menu functions handle navigation

def song_selection_menu():
    """Song selection screen."""
    pygame.display.set_caption("Select Song")

    # Populate songs_list from the SONGS dictionary
    songs_list = [
        {"key": key, "title": song_info["title"], "artist": song_info.get("artist", "Unknown Artist")}
        for key, song_info in SONGS.items()
        if "title" in song_info # Ensure title exists
    ]

    # Check if there are any songs available
    if not songs_list:
        print("[ERROR] No songs found in SONGS dictionary.")
        # Optionally, return to main menu or display an error message
        main_menu()
        return

    # Scrolling state variable
    current_song_index = 0
    
    # Get the initial song info for the button
    initial_song = songs_list[current_song_index]

    # Define button dimensions and gap
    song_button_width = 900 # Much wider button for song title
    song_button_height = 200 # Adjusted height
    arrow_button_width = 80
    arrow_button_height = 50
    horizontal_gap = 50 # Gap between song button and arrow buttons

    # Create the single song button
    song_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), # Centered vertically and horizontally
        text_input=f"{initial_song['title'].upper()}\n{initial_song['artist'].upper()}", # Combined title and artist
        font_size=40, # Adjusted font size for larger button
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"],
        width=song_button_width,
        height=song_button_height
    )

    # Create scroll buttons positioned to the sides of the large song button
    up_arrow_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2 - song_button_width // 2 - horizontal_gap - arrow_button_width // 2, SCREEN_HEIGHT//2 - arrow_button_height // 2), # Position to the left, vertically centered
        text_input="UP", # Could use an image later
        font_size=50,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"],
        width=arrow_button_width,
        height=arrow_button_height
    )

    down_arrow_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2 + song_button_width // 2 + horizontal_gap + arrow_button_width // 2, SCREEN_HEIGHT//2 - arrow_button_height // 2), # Position to the right, vertically centered
        text_input="DOWN", # Could use an image later
        font_size=50,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"],
        width=arrow_button_width,
        height=arrow_button_height
    )
    
    # Back button remains at the bottom
    back_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100), # Position near the bottom
        text_input="BACK",
        font_size=75,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"],
        width=300, # Slightly smaller back button
        height=80
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])

        # Get the current song info
        current_song = songs_list[current_song_index]

        # Display the consistent menu title
        title_text = font_manager.get_font(100).render("SELECT SONG", True, COLORS["GOLD"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(title_text, title_rect)

        # Update the text of the single song button
        song_button.text_input = f"{current_song['title'].upper()}\n{current_song['artist'].upper()}"
        # Re-render the song button to update its text and appearance
        song_button.changeColor(mouse_pos) # This also handles hover color change
        song_button.update(SCREEN)

        # Update and draw scroll buttons conditionally
        if current_song_index > 0:
            up_arrow_button.changeColor(mouse_pos)
            up_arrow_button.update(SCREEN)

        if current_song_index < len(songs_list) - 1:
            down_arrow_button.changeColor(mouse_pos)
            down_arrow_button.update(SCREEN)

        # Update and draw back button
        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check scroll button input only if visible
                if current_song_index > 0 and up_arrow_button.checkForInput(mouse_pos):
                    current_song_index -= 1
                    # Force re-render of the song button with new text (combined title and artist)
                    current_song = songs_list[current_song_index]
                    song_button = Button(
                        image=None,
                        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), # Maintain centered position
                        text_input=f"{current_song['title'].upper()}\n{current_song['artist'].upper()}",
                        font_size=40, # Adjusted font size
                        base_color=COLORS["WHITE"],
                        hovering_color=COLORS["RED"],
                        width=song_button_width,
                        height=song_button_height
                    )
                
                if current_song_index < len(songs_list) - 1 and down_arrow_button.checkForInput(mouse_pos):
                    current_song_index += 1
                    # Force re-render of the song button with new text (combined title and artist)
                    current_song = songs_list[current_song_index]
                    song_button = Button(
                        image=None,
                        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), # Maintain centered position
                        text_input=f"{current_song['title'].upper()}\n{current_song['artist'].upper()}",
                        font_size=40, # Adjusted font size
                        base_color=COLORS["WHITE"],
                        hovering_color=COLORS["RED"],
                        width=song_button_width,
                        height=song_button_height
                    )

                # Check the single song button input
                if song_button.checkForInput(mouse_pos):
                    selected_song_key = songs_list[current_song_index]["key"]
                    pattern_selection(selected_song_key)
                    return

                # Check back button input
                if back_button.checkForInput(mouse_pos):
                    main_menu()
                    return

        pygame.display.update()

def pattern_selection(selected_song):
    """Difficulty selection screen."""
    pygame.display.set_caption("Difficulty")

    # Define fixed button height and gap
    button_height = 90
    button_gap = 30
    button_y_start = 350 # Starting position adjusted for fixed height

    # Create difficulty buttons
    difficulty_buttons = [
        Button(
            image=None,
            pos=(SCREEN_WIDTH//2, button_y_start),
            text_input="EASY",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"],
            width=350, # Fixed width
            height=button_height # Fixed height
        ),
        Button(
            image=None,
            pos=(SCREEN_WIDTH//2, button_y_start + button_height + button_gap),
            text_input="MEDIUM",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"],
            width=350, # Fixed width
            height=button_height # Fixed height
        ),
        Button(
            image=None,
            pos=(SCREEN_WIDTH//2, button_y_start + 2 * (button_height + button_gap)),
            text_input="HARD",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"],
            width=350, # Fixed width
            height=button_height # Fixed height
        )
    ]

    # Back button
    back_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2, button_y_start + 3 * (button_height + button_gap) + 50), # Position after difficulty buttons with extra space
        text_input="BACK",
        font_size=75,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"],
        width=350, # Fixed width
        height=button_height # Fixed height
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])

        # Get song information
        song = SONGS.get(selected_song, {"title": "Unknown Song", "artist": "Unknown Artist"})

        # Draw song title (Header - h1)
        song_title_text = font_manager.get_font(70).render(song['title'].upper(), True, COLORS["GOLD"])
        song_title_rect = song_title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        SCREEN.blit(song_title_text, song_title_rect)

        # Draw difficulty selection text (Subheading - h2)
        difficulty_text = font_manager.get_font(50).render("SELECT DIFFICULTY", True, COLORS["WHITE"])
        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        SCREEN.blit(difficulty_text, difficulty_rect)

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
                if difficulty_buttons[0].checkForInput(mouse_pos):
                    start_game(selected_song, "easy")
                    return
                if difficulty_buttons[1].checkForInput(mouse_pos):
                    start_game(selected_song, "medium")
                    return
                if difficulty_buttons[2].checkForInput(mouse_pos):
                    start_game(selected_song, "hard")
                    return
                if back_button.checkForInput(mouse_pos):
                    song_selection_menu()
                    return

        pygame.display.update()

def endless():
    """Endless mode screen."""
    pygame.display.set_caption("Endless")
    
    # Define fixed button height and gap
    button_height = 90
    button_gap = 30

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
            pos=(SCREEN_WIDTH//2, 400), # Adjusted position
            text_input="BACK",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"],
            width=350, # Fixed width
            height=button_height # Fixed height
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
    pygame.display.set_caption("Main Menu")

    # Define fixed button height and gap
    button_height = 90
    button_gap = 40
    button_y_start = 350 # Adjusted starting position for fixed height

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])

        # Menu title
        menu_text = font_manager.get_font(100).render("RHYTHM GAME", True, COLORS["GOLD"])
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        SCREEN.blit(menu_text, menu_rect)

        # Create buttons with fixed size and adjusted positions
        play_button = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, button_y_start),
            text_input="PLAY",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"],
            width=400,
            height=95
        )
        endless_button = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, button_y_start + button_height + button_gap),
            text_input="ENDLESS",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"],
            width=400,
            height=95
        )
        quit_button = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, button_y_start + 2 * (button_height + button_gap)),
            text_input="QUIT",
            font_size=75,
            base_color=COLORS["WHITE"],
            hovering_color=COLORS["RED"],
            width=400,
            height=95
        )

        # Update and draw buttons
        for button in [play_button, endless_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_pos):
                    song_selection_menu()
                    return
                if endless_button.checkForInput(mouse_pos):
                    start_endless_mode_song_selection() # Call the new endless song selection
                    return
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def start_endless_mode_song_selection():
    """Song selection screen for Endless Mode."""
    pygame.display.set_caption("Select Song (Endless)")

    # Populate songs_list from the SONGS dictionary
    songs_list = [
        {"key": key, "title": song_info["title"], "artist": song_info.get("artist", "Unknown Artist")}
        for key, song_info in SONGS.items()
        if "title" in song_info # Ensure title exists
    ]

    # Check if there are any songs available
    if not songs_list:
        print("[ERROR] No songs found in SONGS dictionary.")
        main_menu()
        return

    # Scrolling state variable
    current_song_index = 0
    
    # Define button dimensions and gap
    song_button_width = 900 # Much wider button for song title
    song_button_height = 200 # Adjusted height
    arrow_button_width = 80
    arrow_button_height = 50
    horizontal_gap = 50 # Gap between song button and arrow buttons

    # Create the single song button
    song_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), # Centered vertically and horizontally
        text_input="", # Text will be updated dynamically
        font_size=40, # Adjusted font size for larger button
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"],
        width=song_button_width,
        height=song_button_height
    )

    # Create scroll buttons positioned to the sides of the large song button
    up_arrow_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2 - song_button_width // 2 - horizontal_gap - arrow_button_width // 2, SCREEN_HEIGHT//2 - arrow_button_height // 2), # Position to the left, vertically centered
        text_input="UP", # Could use an image later
        font_size=50,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"],
        width=arrow_button_width,
        height=arrow_button_height
    )

    down_arrow_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2 + song_button_width // 2 + horizontal_gap + arrow_button_width // 2, SCREEN_HEIGHT//2 - arrow_button_height // 2), # Position to the right, vertically centered
        text_input="DOWN", # Could use an image later
        font_size=50,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"],
        width=arrow_button_width,
        height=arrow_button_height
    )
    
    # Back button remains at the bottom
    back_button = Button(
        image=None,
        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100), # Position near the bottom
        text_input="BACK",
        font_size=75,
        base_color=COLORS["WHITE"],
        hovering_color=COLORS["RED"],
        width=300, # Slightly smaller back button
        height=80
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(COLORS["BLACK"])

        # Get the current song info
        current_song = songs_list[current_song_index]

        # Display the consistent menu title
        title_text = font_manager.get_font(100).render("SELECT SONG", True, COLORS["GOLD"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(title_text, title_rect)

        # Update the text of the single song button
        song_button.text_input = f"{current_song["title"].upper()}\n{current_song.get("artist", "Unknown Artist").upper()}"
        # Re-render the song button to update its text and appearance
        song_button.changeColor(mouse_pos) # This also handles hover color change
        song_button.update(SCREEN)

        # Update and draw scroll buttons conditionally
        if current_song_index > 0:
            up_arrow_button.changeColor(mouse_pos)
            up_arrow_button.update(SCREEN)

        if current_song_index < len(songs_list) - 1:
            down_arrow_button.changeColor(mouse_pos)
            down_arrow_button.update(SCREEN)

        # Update and draw back button
        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check scroll button input only if visible
                if current_song_index > 0 and up_arrow_button.checkForInput(mouse_pos):
                    current_song_index -= 1
                    # Force re-render of the song button with new text
                    current_song = songs_list[current_song_index]
                    song_button = Button(
                        image=None,
                        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), # Maintain centered position
                        text_input=f"{current_song["title"].upper()}\n{current_song.get("artist", "Unknown Artist").upper()}",
                        font_size=40, # Adjusted font size
                        base_color=COLORS["WHITE"],
                        hovering_color=COLORS["RED"],
                        width=song_button_width,
                        height=song_button_height
                    )
                
                if current_song_index < len(songs_list) - 1 and down_arrow_button.checkForInput(mouse_pos):
                    current_song_index += 1
                    # Force re-render of the song button with new text
                    current_song = songs_list[current_song_index]
                    song_button = Button(
                        image=None,
                        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), # Maintain centered position
                        text_input=f"{current_song["title"].upper()}\n{current_song.get("artist", "Unknown Artist").upper()}",
                        font_size=40, # Adjusted font size
                        base_color=COLORS["WHITE"],
                        hovering_color=COLORS["RED"],
                        width=song_button_width,
                        height=song_button_height
                    )

                # Check the single song button input
                if song_button.checkForInput(mouse_pos):
                    selected_song_key = songs_list[current_song_index]["key"]
                    # Start the game in endless mode
                    start_game(selected_song_key, "endless") # Pass 'endless' as difficulty/mode
                    return

                # Check back button input
                if back_button.checkForInput(mouse_pos):
                    main_menu()
                    return

        pygame.display.update() 