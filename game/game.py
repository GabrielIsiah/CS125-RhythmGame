import pygame
import sys
from game.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, ARROW_SPEED,
    HIT_FEEDBACK_DURATION, MUSIC_START_DELAY
)
from game.hit_detection import HitDetector
from game.arrow_spawner import ArrowSpawner
from game.outline_manager import OutlineManager

class Game:
    def __init__(self, outlines, arrows):
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
        pygame.mixer.music.load('song.mp3')
        self.music = pygame.mixer.Sound('song.mp3')
        self.music_started = False
        
        # Set up display elements
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background.fill('White')
        self.font = pygame.font.SysFont(None, 48)
        self.combo_font = pygame.font.SysFont(None, 72)  # Larger font for combo display
        
        # Initialize game state
        self.start_ticks = pygame.time.get_ticks()
        self.running = True
        
        # Load game data
        self.arrow_spawner.add_timestamps()
        self.outline_manager.add_outlines(self.outline_group)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
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
            self.music.play()
            self.music.set_volume(0.3)
            self.music_started = True

        # Update arrow positions and check for misses
        for arrow in self.arrow_group:
            arrow.update(ARROW_SPEED)
            # Check if arrow has passed the hit zone (outline)
            outline = next((o for o in self.outline_group if o.key == arrow.key), None)
            if outline and arrow.rect.top > outline.rect.bottom:
                self.hit_detector.check_miss(arrow)
                self.arrow_group.remove(arrow)

        # Spawn new arrows
        self.arrow_spawner.spawn_arrow(elapsed_sec, self.arrow_group)

    def draw(self):
        # Clear screen
        self.display.blit(self.background, (0, 0))

        # Draw timer
        elapsed_sec = (pygame.time.get_ticks() - self.start_ticks) / 1000
        timer_text = self.font.render(f"Time: {elapsed_sec:.2f}s", True, (255, 0, 0))
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
                feedback_y = 50  # Position it higher up
                self.display.blit(feedback_text, (feedback_x, feedback_y))
            else:
                self.hit_detector.hit_feedback = ""
                self.hit_detector.hit_type = ""
                self.hit_detector.hit_color = (0, 0, 0)
                self.hit_detector.combo_hits = 0
                self.hit_detector.combo_score = 0

        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS) 