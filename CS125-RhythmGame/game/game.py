import pygame
import sys
import os
from game.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, DIFFICULTY_SPEEDS,
    HIT_FEEDBACK_DURATION, MUSIC_START_DELAY
)
from game.hit_detection import HitDetector
from game.arrow_spawner import ArrowSpawner
from game.outline_manager import OutlineManager
from Utility.font_manager import font_manager

class Game:
    def __init__(self, outlines, arrows, song_key="song1", difficulty="easy"):
        # Initialize pygame components
        pygame.mixer.init()
        
        # Set up display (already initialized in main.py)
        self.display = pygame.display.get_surface()
        pygame.display.set_caption('Rhythm Game')
        
        # Initialize game components
        self.arrow_group = pygame.sprite.Group()
        self.outline_group = pygame.sprite.Group()
        self.hit_detector = HitDetector()
        self.arrow_spawner = ArrowSpawner(arrows)
        self.outline_manager = OutlineManager(outlines)
        
        # Set up music
        self.music_path = os.path.join('assets', 'audio', 'song.mp3')
        pygame.mixer.music.load(self.music_path)
        self.music_started = False
        self.music_position = 0  # Store music position for pause/resume
        
        # Set up display elements
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background.fill('White')
        self.font = font_manager.get_font(48)
        self.combo_font = font_manager.get_font(72)  # Larger font for combo display
        
        # Initialize game state
        self.start_ticks = pygame.time.get_ticks()
        self.running = True
        self.song_key = song_key
        self.difficulty = difficulty
        self.arrow_speed = DIFFICULTY_SPEEDS[difficulty]
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
        
        # Load game data
        if song_key == "pattern":  # Use pattern system instead of CSV
            self.arrow_spawner.start_pattern_mode(difficulty)
        else:
            self.arrow_spawner.add_timestamps()
        self.outline_manager.add_outlines(self.outline_group)

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
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)
            self.music_started = True

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

        # Detect end of song (music stopped)
        if self.music_started and not pygame.mixer.music.get_busy() and not self.waiting_for_results and not self.paused:
            self.final_score = self.hit_detector.score
            self.final_time = elapsed_sec
            self.song_end_time = pygame.time.get_ticks()
            # Capture the last frame
            self.last_frame = self.display.copy()
            self.waiting_for_results = True
            return

        # Update arrow positions and check for misses
        for arrow in self.arrow_group:
            arrow.update(self.arrow_speed)
            # Check if arrow has passed the hit zone (outline)
            outline = next((o for o in self.outline_group if o.key == arrow.key), None)
            if outline and arrow.rect.top > outline.rect.bottom:
                self.hit_detector.check_miss(arrow)
                self.arrow_group.remove(arrow)

        # Spawn new arrows
        self.arrow_spawner.spawn_arrow(elapsed_sec, self.arrow_group)

    def init_results_popup(self):
        # Centered popup with score and 3 buttons
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        button_gap = 90
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

    def draw_results_popup(self):
        # Dim background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.display.blit(overlay, (0,0))
        # Popup box
        popup_rect = pygame.Rect(WINDOW_WIDTH//2-250, WINDOW_HEIGHT//2-200, 500, 400)
        pygame.draw.rect(self.display, (40,40,40), popup_rect, border_radius=20)
        pygame.draw.rect(self.display, (200,200,200), popup_rect, 4, border_radius=20)
        # Score
        score_text = self.results_font.render(f"Score: {self.final_score}", True, (255,255,0))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2-80))
        self.display.blit(score_text, score_rect)
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.results_buttons:
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
                        # Placeholder: print which button was pressed
                        print(f"Button pressed: {btn['label']}")
                        # Actions will be implemented later

    def draw(self):
        # If results popup is showing, blit the last frame and return
        if self.show_results and self.last_frame is not None:
            self.display.blit(self.last_frame, (0, 0))
            return
        # If paused, blit the pause frame and return
        if self.paused and self.pause_frame is not None:
            self.display.blit(self.pause_frame, (0, 0))
            return
        # Clear screen
        self.display.blit(self.background, (0, 0))

        # Draw timer
        elapsed_sec = (pygame.time.get_ticks() - self.start_ticks) / 1000
        timer_to_show = self.final_time if self.show_results else elapsed_sec
        timer_text = self.font.render(f"Time: {timer_to_show:.2f}s", True, (255, 0, 0))
        self.display.blit(timer_text, (100, 80))

        # Draw score
        score_text = self.font.render(f"Score: {self.hit_detector.score}", True, (0, 0, 255))
        self.display.blit(score_text, (100, 130))

        # Draw combo counter
        if self.hit_detector.combo > 0:
            combo_text = self.combo_font.render(f"{self.hit_detector.combo} Combo", True, (255, 165, 0))  # Orange color
            self.display.blit(combo_text, (50, WINDOW_HEIGHT - 100))  # Bottom left position

        # Draw game elements
        self.outline_group.draw(self.display)
        self.arrow_group.draw(self.display)

        # Show hit feedback if active
        if self.hit_detector.hit_feedback:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_detector.hit_feedback_timer < HIT_FEEDBACK_DURATION:
                feedback_text = self.font.render(self.hit_detector.hit_feedback, True, self.hit_detector.hit_color)
                # Center the feedback text horizontally and position it near the top
                feedback_x = (WINDOW_WIDTH - feedback_text.get_width()) // 2
                self.display.blit(feedback_text, (feedback_x, 200))

        pygame.display.update()

    def cleanup(self):
        if self.song_key == "pattern":
            self.arrow_spawner.stop_pattern_mode()

    def pause_game(self):
        if not self.paused:  # Only pause if not already paused
            self.paused = True
            # Store the current game state
            self.pause_time = pygame.time.get_ticks() - self.start_ticks
            # Store current music position
            self.music_position = pygame.mixer.music.get_pos() / 1000.0
            pygame.mixer.music.pause()
            # Capture the current frame for pause background
            self.pause_frame = self.display.copy()
            self.init_pause_popup()

    def resume_game(self):
        if self.paused:  # Only resume if currently paused
            self.paused = False
            # Adjust start_ticks to maintain the same elapsed time
            self.start_ticks = pygame.time.get_ticks() - self.pause_time
            # Resume music from stored position
            pygame.mixer.music.unpause()

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
                'label': 'QUIT',
                'rect': pygame.Rect(center_x-150, center_y+40+button_gap, 300, 70),
                'hover': False
            }
        ]

    def draw_pause_popup(self):
        # Dim background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.display.blit(overlay, (0,0))
        # Popup box
        popup_rect = pygame.Rect(WINDOW_WIDTH//2-250, WINDOW_HEIGHT//2-200, 500, 300)
        pygame.draw.rect(self.display, (40,40,40), popup_rect, border_radius=20)
        pygame.draw.rect(self.display, (200,200,200), popup_rect, 4, border_radius=20)
        # Pause text
        pause_text = self.pause_font.render("PAUSED", True, (255,255,0))
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2-80))
        self.display.blit(pause_text, pause_rect)
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.pause_buttons:
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
                        elif btn['label'] == 'QUIT':
                            self.running = False
                        return

    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            if self.show_results:
                self.handle_results_popup_events()
                self.draw()
                self.draw_results_popup()
                pygame.display.update()
                clock.tick(FPS)
                continue
            if self.paused:
                self.handle_pause_popup_events()
                self.draw()
                self.draw_pause_popup()
                pygame.display.update()
                clock.tick(FPS)
                continue
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            clock.tick(FPS) 