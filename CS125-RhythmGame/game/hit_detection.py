from game.constants import (
    HIT_MARGIN_PERFECT,
    HIT_MARGIN_GOOD,
    HIT_MARGIN_LATE,
    SCORE_PERFECT,
    SCORE_GOOD,
    SCORE_LATE,
    SCORE_MISS
)
import pygame
from Utility.audio_manager import audio_manager
import threading
import queue
import time

class HitDetector:
    def __init__(self):
        self.score = 0
        self.hit_feedback = ""
        self.hit_feedback_timer = 0
        self.hit_type = ""
        self.hit_color = (0, 0, 0)  # Default color
        self.combo = 0  # Track current combo
        self.max_combo = 0  # Track highest combo achieved
        self.combo_hits = 0
        self.combo_score = 0
        self.misses = 0  # Track total misses
        
        # Thread-safe queues for communication between threads
        self.key_press_queue = queue.Queue()
        self.hit_margin_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        # Thread control
        self.running = True
        
        # Start worker threads
        self.key_press_thread = threading.Thread(target=self._process_key_presses, daemon=True)
        self.hit_margin_thread = threading.Thread(target=self._process_hit_margins, daemon=True)
        self.key_press_thread.start()
        self.hit_margin_thread.start()

    def _process_key_presses(self):
        """Thread for processing key presses and initial hit detection."""
        while self.running:
            try:
                key_data = self.key_press_queue.get(timeout=0.1)
                key, arrow_group, outline_group = key_data
                
                # Find possible hits for this key
                possible_hits = [arrow for arrow in arrow_group if arrow.key == key]
                if not possible_hits:
                    self._handle_miss()
                    continue
                
                # Find outline for this key
                outline_sprite = next((o for o in outline_group if o.key == key), None)
                if not outline_sprite:
                    self._handle_miss()
                    continue
                
                # Sort arrows by distance to outline center y
                possible_hits.sort(key=lambda a: abs(a.hitbox.centery - outline_sprite.rect.centery))
                closest_arrow = possible_hits[0]
                
                # Check if hitboxes overlap horizontally
                if not (closest_arrow.hitbox.right >= outline_sprite.rect.left and 
                        closest_arrow.hitbox.left <= outline_sprite.rect.right):
                    self._handle_miss()
                    continue
                
                # Calculate vertical overlap
                vertical_overlap = min(closest_arrow.hitbox.bottom, outline_sprite.rect.bottom) - max(closest_arrow.hitbox.top, outline_sprite.rect.top)
                if vertical_overlap <= 0:
                    self._handle_miss()
                    continue
                
                # Send to hit margin thread for timing calculation
                self.hit_margin_queue.put((closest_arrow, outline_sprite, arrow_group))
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in key press thread: {e}")
                continue

    def _process_hit_margins(self):
        """Thread for calculating hit margins and determining hit types."""
        while self.running:
            try:
                margin_data = self.hit_margin_queue.get(timeout=0.1)
                arrow, outline, arrow_group = margin_data
                
                # Calculate center distance and determine if hit is early or late
                center_dist = abs(arrow.hitbox.centery - outline.rect.centery)
                is_late = arrow.hitbox.centery > outline.rect.centery
                
                # Check if arrow is within the outline's vertical bounds
                is_within_outline = (arrow.hitbox.bottom >= outline.rect.top and 
                                   arrow.hitbox.top <= outline.rect.bottom)
                
                # Determine hit type based on timing and position
                if center_dist <= HIT_MARGIN_PERFECT:
                    self._handle_hit("Perfect", SCORE_PERFECT, (0, 255, 0), 'perfect', arrow_group, arrow)
                elif center_dist <= HIT_MARGIN_GOOD:
                    self._handle_hit("Good", SCORE_GOOD, (255, 255, 0), 'good', arrow_group, arrow)
                elif is_within_outline and center_dist <= HIT_MARGIN_LATE:
                    self._handle_hit("Late" if is_late else "Early", SCORE_LATE, (255, 0, 0), 'good', arrow_group, arrow)
                else:
                    self._handle_miss()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in hit margin thread: {e}")
                continue

    def _handle_hit(self, hit_type, base_score, color, sound, arrow_group, arrow):
        """Handle a successful hit."""
        self.hit_type = hit_type
        self.hit_color = color
        self.hit_feedback = hit_type
        self.hit_feedback_timer = pygame.time.get_ticks()
        self.score += self.apply_score(base_score)
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        audio_manager.play_sound(sound)
        arrow_group.remove(arrow)

    def _handle_miss(self):
        """Handle a miss."""
        self.combo = 0
        self.hit_type = "Miss"
        self.hit_color = (128, 128, 128)
        self.hit_feedback = "Miss"
        self.hit_feedback_timer = pygame.time.get_ticks()
        self.score += SCORE_MISS
        self.misses += 1
        audio_manager.play_sound('miss')

    def check_hit(self, key, arrow_group, outline_group):
        """Queue a hit check for processing."""
        self.key_press_queue.put((key, arrow_group, outline_group))

    def check_miss(self, arrow):
        """Handle a miss when an arrow passes the hit zone."""
        self._handle_miss()

    def cleanup(self):
        """Clean up resources when the game ends."""
        self.running = False
        if self.key_press_thread:
            self.key_press_thread.join(timeout=1.0)
        if self.hit_margin_thread:
            self.hit_margin_thread.join(timeout=1.0)

    def get_combo_multiplier(self):
        """Calculate the current combo multiplier."""
        if self.combo >= 300:
            return 4
        elif self.combo >= 200:
            return 3
        elif self.combo >= 100:
            return 2
        return 1

    def apply_score(self, base_score):
        """Apply the current combo multiplier to the score."""
        multiplier = self.get_combo_multiplier()
        return base_score * multiplier 