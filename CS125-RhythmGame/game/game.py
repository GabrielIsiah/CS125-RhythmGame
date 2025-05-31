import pygame
import sys
import os
import random
from game.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, DIFFICULTY_SPEEDS,
    HIT_FEEDBACK_DURATION, MUSIC_START_DELAY,
    GRAVITY_MIN_DURATION, GRAVITY_MAX_DURATION,
    GRAVITY_NORMAL_MIN_DURATION, GRAVITY_NORMAL_MAX_DURATION,
    SCORE_POSITION, MISS_POSITION, COMBO_POSITION, FEEDBACK_POSITION,
    NORMAL_HIT_ZONE_Y, GRAVITY_HIT_ZONE_Y, GRAVITY_SAFE_INTERVAL,
    VIDEO_START_DELAY
)
from game.hit_detection import HitDetector
from game.arrow_spawner import ArrowSpawner
from game.outline_manager import OutlineManager
from Utility.font_manager import font_manager
from Utility.audio_manager import audio_manager
from game.pyvidplayer import Video
# SONGS will be passed in from the menu
# from game.menu import SONGS

class Game:
    def __init__(self, outlines, arrows, songs_data, song_key="song1", difficulty="easy", mode="normal"):
        # Initialize pygame components
        pygame.mixer.init()
        
        # Store songs data
        self.songs_data = songs_data

        # Set up display (already initialized in main.py)
        self.display = pygame.display.get_surface()
        pygame.display.set_caption('Rhythm Game')
        
        # Initialize game components
        self.arrow_group = pygame.sprite.Group()
        self.outline_group = pygame.sprite.Group()
        self.hit_detector = HitDetector()
        # Pass the selected song_key and songs_data to the ArrowSpawner
        self.arrow_spawner = ArrowSpawner(arrows, self.songs_data)
        self.arrow_spawner.difficulty = difficulty  # Set the difficulty in ArrowSpawner
        self.outline_manager = OutlineManager(outlines)
        
        # Set up music
        # Get music file path from songs_data dictionary
        song_info = self.songs_data.get(song_key)
        if song_info and "music_file" in song_info:
            self.music_path = os.path.join(song_info["music_file"])
        else:
            self.music_path = None # Or set a default error sound
            
        self.music_started = False
        self.music_position = 0  # Store music position for pause/resume
        
        # Set up display elements
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background.fill('White')
        self.font = font_manager.get_font(36)  # Smaller font for UI
        self.combo_font = font_manager.get_font(48)  # Smaller font for combo
        
        # Initialize game state
        self.start_ticks = pygame.time.get_ticks()
        self.running = True
        self.song_key = song_key
        self.difficulty = difficulty
        self.arrow_speed = DIFFICULTY_SPEEDS.get(difficulty, DIFFICULTY_SPEEDS['easy'])
        self.show_results = False
        self.waiting_for_results = False
        self.song_end_time = None
        self.final_time = 0.0
        self.last_frame = None
        self.results_buttons = []
        self.results_font = font_manager.get_font(72)
        self.results_small_font = font_manager.get_font(48)
        self.final_score = 0
        self.paused = False
        self.pause_frame = None
        self.pause_buttons = []
        self.pause_font = font_manager.get_font(72)
        self.pause_small_font = font_manager.get_font(48)
        self.mode = mode
        self.next_action = None

        # Load background video
        video_path = os.path.join('assets', 'vids', 'song.mp4')
        try:
            self.background_video = Video(video_path)
            # Optionally resize the video to fit the screen
            self.background_video.set_size((WINDOW_WIDTH, WINDOW_HEIGHT))
            # Pause the video immediately
            self.background_video.toggle_pause()
        except FileNotFoundError:
            print(f"[WARNING] Background video not found at {video_path}")
            self.background_video = None

        # Gravity mode settings (for medium difficulty)
        self.gravity_mode = False
        self.gravity_mode_start = 0
        self.gravity_mode_duration = 0
        self.next_gravity_switch = 0
        
        # Add countdown variables
        self.show_countdown = False
        self.countdown_start = 0
        self.countdown_duration = 5000  # 5 seconds in milliseconds
        self.countdown_font = font_manager.get_font(72)  # Larger font for countdown
        
        # Load game data
        if song_key == "pattern":
            self.arrow_spawner.start_pattern_mode(difficulty)
        else:
            if self.mode == "normal":
                self.arrow_spawner.add_timestamps(song_key)
            else:
                self.arrow_spawner.add_timestamps(song_key)

        # Initialize hit zones based on difficulty
        if self.difficulty == "medium" or self.difficulty == "hard":
            # Start with normal mode, schedule first gravity switch
            self.gravity_mode = False
            self.schedule_next_gravity_switch()
        else:
            # For other difficulties, always use normal mode
            self.gravity_mode = False

        self.outline_manager.add_outlines(self.outline_group, self.gravity_mode)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Add escape key to pause
                    if not self.paused and not self.show_results:
                        self.pause_game()
                    elif self.paused:
                        self.resume_game()
                    return
                elif not self.paused and not self.show_results:
                    if event.key == pygame.K_d:
                        self.hit_detector.check_hit('d', self.arrow_group, self.outline_group)
                    elif event.key == pygame.K_f:
                        self.hit_detector.check_hit('f', self.arrow_group, self.outline_group)
                    elif event.key == pygame.K_j:
                        self.hit_detector.check_hit('j', self.arrow_group, self.outline_group)
                    elif event.key == pygame.K_k:
                        self.hit_detector.check_hit('k', self.arrow_group, self.outline_group)

    def update(self):
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        elapsed_sec = elapsed_ms / 1000

        # Start music after delay
        if elapsed_sec >= MUSIC_START_DELAY and not self.music_started:
            try:
                audio_manager.play_music(self.music_path)
                self.music_started = True
            except Exception as e:
                print(f"[ERROR] Failed to play music: {e}")

        # Unpause video after delay if it's paused
        if self.background_video and self.background_video.get_playback_data()['paused'] and elapsed_sec >= VIDEO_START_DELAY:
             self.background_video.toggle_pause()

        # Update video frames if game is running and video is active
        if not self.paused and not self.show_results and self.background_video and self.background_video.active:
             self.background_video.update()

        # Check for gravity mode switch
        self.check_gravity_switch()

        # If results popup is showing, do not update game state
        if self.show_results:
            return

        # If waiting for results, check delay
        if self.waiting_for_results:
            if pygame.time.get_ticks() - self.song_end_time >= 1000:
                self.show_results = True
                self.waiting_for_results = False
                self.init_results_popup()
            return

        # Detect end of song (music stopped) - only in normal mode
        if self.mode == "normal":
            if self.music_started and not pygame.mixer.music.get_busy() and not self.waiting_for_results and not self.paused:
                self.final_score = self.hit_detector.score
                self.final_time = elapsed_sec
                self.song_end_time = pygame.time.get_ticks()
                self.last_frame = self.display.copy()
                self.waiting_for_results = True
                self.arrow_group.empty()
                self.arrow_spawner.spawning_allowed = False
                return

        # Update arrow positions and check for misses
        for arrow in list(self.arrow_group.sprites()):  # Create a copy of the sprite list
            # Reverse direction in gravity mode
            speed = -self.arrow_speed if self.gravity_mode else self.arrow_speed
            arrow.update(speed)
            
            # Check if arrow has passed the hit zone
            outline = next((o for o in self.outline_group if o.key == arrow.key), None)
            if outline:
                if self.gravity_mode:
                    if arrow.rect.bottom < outline.rect.top:
                        self.hit_detector.check_miss(arrow)
                        arrow.kill()  # This will remove the sprite from all groups
                else:
                    if arrow.rect.top > outline.rect.bottom:
                        self.hit_detector.check_miss(arrow)
                        arrow.kill()  # This will remove the sprite from all groups

        # Spawn new arrows
        self.arrow_spawner.spawn_arrow(elapsed_sec, self.arrow_group, self.gravity_mode)

    def init_results_popup(self):
        # Centered popup with score and 3 buttons
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        button_gap = 90

        # Define buttons based on mode
        if self.mode == "normal":
            self.results_buttons = [
                {
                    'label': 'RESTART',
                    'rect': pygame.Rect(center_x-150, center_y+40, 300, 70),
                    'hover': False
                },
                {
                    'label': 'DIFFICULTY',
                    'rect': pygame.Rect(center_x-150, center_y+40+button_gap, 300, 70),
                    'hover': False
                },
                {
                    'label': 'QUIT',
                    'rect': pygame.Rect(center_x-150, center_y+40+2*button_gap, 300, 70),
                    'hover': False
                }
            ]
        # In endless mode, define a different set of buttons, maybe just QUIT and RESTART Endless
        elif self.mode == "endless":
             self.results_buttons = [
                {
                    'label': 'RESTART ENDLESS',
                    'rect': pygame.Rect(center_x-150, center_y+40, 300, 70),
                    'hover': False
                },
                {
                    'label': 'QUIT',
                    'rect': pygame.Rect(center_x-150, center_y+40+button_gap, 300, 70),
                    'hover': False
                }
             ]

    def draw_results_popup(self):
        # Dim background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.display.blit(overlay, (0,0))
        # Popup box
        popup_rect = pygame.Rect(WINDOW_WIDTH//2-275, WINDOW_HEIGHT//2-250, 550, 500) # Increased width to 550 and adjusted x for centering
        pygame.draw.rect(self.display, (40,40,40), popup_rect, border_radius=20)
        pygame.draw.rect(self.display, (200,200,200), popup_rect, 4, border_radius=20)
        # Score
        score_text = self.results_font.render(f"Score: {self.final_score}", True, (255,255,0))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2-150))
        self.display.blit(score_text, score_rect)
        # Buttons
        mouse_pos = pygame.mouse.get_pos()


        # Let's try placing the first button closer to the score
        button_y_start = WINDOW_HEIGHT//2 - 20 # Adjusted starting position for buttons (moved upwards)
        button_gap = 100 # Keep existing button gap
        
        for i, btn in enumerate(self.results_buttons):
            # Adjust button vertical position based on the new starting point and gap
            btn['rect'].center = (WINDOW_WIDTH//2, button_y_start + i * button_gap)
            btn['hover'] = btn['rect'].collidepoint(mouse_pos)
            color = (255,0,0) if btn['hover'] else (255,255,255)
            pygame.draw.rect(self.display, color, btn['rect'], border_radius=10, width=3)
            label = self.results_small_font.render(btn['label'], True, color)
            label_rect = label.get_rect(center=btn['rect'].center)
            self.display.blit(label, label_rect)

    def handle_results_popup_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.results_buttons:
                    if btn['hover']:
                        # Handle button actions based on mode
                        if self.mode == "normal":
                            if btn['label'] == 'RESTART':
                                # Restart the current song and difficulty
                                self.running = False # Stop the current game instance
                                # The start_game function in menu.py will be called after this instance ends
                                # with the same song_key and difficulty
                                self.next_action = 'restart'
                            elif btn['label'] == 'DIFFICULTY':
                                # Go back to difficulty selection for the current song
                                self.running = False # Stop the current game instance
                                # The song_selection_menu will be called after this instance ends,
                                # and then pattern_selection will be called from there.
                                # We need a way to pass the selected_song_key back.
                                # This might require restructuring the menu flow slightly.
                                # For now, we'll just go back to main menu as a temporary measure.
                                # TODO: Implement proper return to difficulty selection.
                                # For now, setting running to False and letting menu handle the return
                                pass # Let the menu handle returning
                            elif btn['label'] == 'QUIT':
                                self.running = False # Stop the current game instance
                                # The main_menu will be called after this instance ends.
                                self.next_action = 'quit'
                        elif self.mode == "endless":
                             if btn['label'] == 'RESTART ENDLESS':
                                 # Restart endless mode with the same song
                                 self.running = False
                                 # start_game with endless mode and same song will be called from menu
                                 self.next_action = 'restart_endless'
                             elif btn['label'] == 'QUIT':
                                 self.running = False
                                 # main_menu will be called from menu
                        return # Exit event handling after a button is pressed

    def draw(self):
        # If results popup is showing, blit the last frame and return - only in normal mode
        if self.mode == "normal" and self.show_results and self.last_frame is not None:
            self.display.blit(self.last_frame, (0, 0))
            return
        # If paused, blit the pause frame and return
        if self.paused and self.pause_frame is not None:
            self.display.blit(self.pause_frame, (0, 0))
            return

        # Get elapsed time
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        elapsed_sec = elapsed_ms / 1000

        # Draw background video if not paused or showing results and after delay
        if not self.paused and not self.show_results and self.background_video and elapsed_sec >= VIDEO_START_DELAY:
            self.background_video.draw(self.display, (0, 0))
        elif not self.paused and not self.show_results and elapsed_sec < VIDEO_START_DELAY:
            # Draw black background before video starts
            self.display.fill((0, 0, 0)) # Fill with black
        else:
            # Clear screen with background color if no video or paused/results
            self.display.blit(self.background, (0, 0))

        # Draw score
        score_text = self.font.render(f"Score: {self.hit_detector.score}", True, (0, 0, 255))
        self.display.blit(score_text, SCORE_POSITION)

        # Draw miss counter
        miss_text = self.font.render(f"Misses: {self.hit_detector.misses}", True, (0, 0, 255))
        self.display.blit(miss_text, MISS_POSITION)

        # Draw combo counter
        if self.hit_detector.combo > 0:
            combo_text = self.combo_font.render(f"{self.hit_detector.combo} Combo", True, (255, 165, 0))
            self.display.blit(combo_text, COMBO_POSITION)

        # Draw game elements
        self.outline_group.draw(self.display)
        self.arrow_group.draw(self.display)

        # Show hit feedback if active
        if self.hit_detector.hit_feedback:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_detector.hit_feedback_timer < HIT_FEEDBACK_DURATION:
                feedback_text = self.font.render(self.hit_detector.hit_feedback, True, self.hit_detector.hit_color)
                feedback_x = (WINDOW_WIDTH - feedback_text.get_width()) // 2
                self.display.blit(feedback_text, (feedback_x, FEEDBACK_POSITION[1]))

        # Draw countdown if active
        if self.show_countdown:
            current_time = pygame.time.get_ticks()
            time_left = (self.countdown_duration - (current_time - self.countdown_start)) / 1000
            if time_left > 0:
                # Draw countdown in top center of screen
                countdown_text = self.countdown_font.render(f"{int(time_left) + 1}", True, (255, 255, 0))
                countdown_rect = countdown_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
                
                # Draw semi-transparent background for countdown
                countdown_bg = pygame.Surface((countdown_rect.width + 20, countdown_rect.height + 20), pygame.SRCALPHA)
                countdown_bg.fill((0, 0, 0, 128))
                self.display.blit(countdown_bg, (countdown_rect.centerx - countdown_bg.get_width() // 2, 
                                               countdown_rect.centery - countdown_bg.get_height() // 2))
                
                # Draw countdown text
                self.display.blit(countdown_text, countdown_rect)

        pygame.display.update()

    def cleanup(self):
        if self.song_key == "pattern":
            self.arrow_spawner.stop_pattern_mode()
        audio_manager.cleanup()
        # Close the video player
        if self.background_video:
            self.background_video.close()

    def pause_game(self):
        if not self.paused:  # Only pause if not already paused
            self.paused = True
            # Store the current game state
            self.pause_time = pygame.time.get_ticks() - self.start_ticks
            # Store current music position
            if self.music_started:
                 self.music_position = pygame.mixer.music.get_pos() / 1000.0
                 audio_manager.pause_music()
            # Capture the current frame for pause background
            self.pause_frame = self.display.copy()
            self.init_pause_popup()

    def resume_game(self):
        if self.paused:  # Only resume if currently paused
            self.paused = False
            # Adjust start_ticks to maintain the same elapsed time
            self.start_ticks = pygame.time.get_ticks() - self.pause_time
            # Resume music from stored position
            if self.music_started:
                 audio_manager.unpause_music()

    def init_pause_popup(self):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        button_gap = 90
        self.pause_buttons = [
            {
                'label': 'RESUME',
                'rect': pygame.Rect(center_x-150, center_y+40, 300, 70),
                'hover': False
            },
            {
                'label': 'RETRY',
                'rect': pygame.Rect(center_x-150, center_y+40+button_gap, 300, 70),
                'hover': False
            },
            {
                'label': 'QUIT',
                'rect': pygame.Rect(center_x-150, center_y+40+2*button_gap, 300, 70),
                'hover': False
            }
        ]

    def draw_pause_popup(self):
        # Dim background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.display.blit(overlay, (0,0))
        # Popup box
        popup_rect = pygame.Rect(WINDOW_WIDTH//2-250, WINDOW_HEIGHT//2-250, 500, 500) # Adjusted position and height
        pygame.draw.rect(self.display, (40,40,40), popup_rect, border_radius=20)
        pygame.draw.rect(self.display, (200,200,200), popup_rect, 4, border_radius=20)
        # Pause text
        pause_text = self.pause_font.render("PAUSED", True, (255,255,0))
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2-150)) # Adjusted vertical position
        self.display.blit(pause_text, pause_rect)
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        button_y_start = WINDOW_HEIGHT//2 - 40 # Adjusted starting position for buttons
        button_gap = 90 # Keep existing button gap
        for i, btn in enumerate(self.pause_buttons):
            # Adjust button vertical position based on the new popup height and arrangement
            btn['rect'].center = (WINDOW_WIDTH//2, button_y_start + i * button_gap) # Adjust button vertical spacing
            btn['hover'] = btn['rect'].collidepoint(mouse_pos)
            color = (255,0,0) if btn['hover'] else (255,255,255)
            pygame.draw.rect(self.display, color, btn['rect'], border_radius=10, width=3)
            label = self.pause_small_font.render(btn['label'], True, color)
            label_rect = label.get_rect(center=btn['rect'].center)
            self.display.blit(label, label_rect)

    def handle_pause_popup_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.pause_buttons:
                    if btn['hover']:
                        if btn['label'] == 'RESUME':
                            self.resume_game()
                        elif btn['label'] == 'RETRY':
                            self.running = False
                            self.next_action = 'restart'
                        elif btn['label'] == 'QUIT':
                            self.running = False
                            self.next_action = 'quit'
                        return

    def schedule_next_gravity_switch(self):
        """Schedule the next gravity mode switch."""
        current_time = pygame.time.get_ticks()
        
        # Random duration between 15-30 seconds
        duration = random.uniform(15.0, 30.0)
        
        self.next_gravity_switch = current_time + (duration * 1000)

    def check_gravity_switch(self):
        """Check if it's time to switch gravity mode."""
        if not (self.difficulty == "medium" or self.difficulty == "hard"):
            return
            
        current_time = pygame.time.get_ticks()
        
        # If countdown is active, check if it's time to switch
        if self.show_countdown:
            if current_time - self.countdown_start >= self.countdown_duration:
                # Switch modes
                self.gravity_mode = not self.gravity_mode
                self.outline_manager.update_outline_positions(self.outline_group, self.gravity_mode)
                self.schedule_next_gravity_switch()
                self.show_countdown = False
            return
            
        # Check if it's time to start countdown
        if current_time >= self.next_gravity_switch:
            self.show_countdown = True
            self.countdown_start = current_time

    def is_safe_to_switch(self):
        """Always return True since we're using countdown instead of arrow checks."""
        return True

    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            # Only show results popup in normal mode
            if self.mode == "normal" and self.show_results: # Add mode check
                self.handle_results_popup_events()
                self.draw()
                self.draw_results_popup()
                pygame.display.update()
                clock.tick(FPS)
                continue
            # Pause logic applies to both modes
            if self.paused:
                self.handle_pause_popup_events()
                self.draw()
                self.draw_pause_popup()
                pygame.display.update()
                clock.tick(FPS)
                continue
            
            self.handle_events()
            # Only update game state if not showing results (which won't happen in endless mode anyway)
            if not self.show_results:
                self.update()
            
            self.draw()
            pygame.display.update()
            clock.tick(FPS)
        return self.next_action # Return the action requested by the user 