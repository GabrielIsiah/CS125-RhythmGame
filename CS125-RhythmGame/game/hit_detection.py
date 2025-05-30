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

    def check_miss(self, arrow):
        """Handle missed arrows that pass the hit zone"""
        self.combo = 0  # Reset combo on miss
        self.hit_type = "Miss"
        self.hit_color = (128, 128, 128)  # Gray color for misses
        self.hit_feedback = "Miss"
        self.hit_feedback_timer = pygame.time.get_ticks()
        self.score += SCORE_MISS
        self.misses += 1  # Increment miss counter
        audio_manager.play_sound('miss')  # Play miss sound
        return True

    def check_hit(self, key, arrow_group, outline_group):
        print(f"Checking hits for key '{key}'")

        possible_hits = [arrow for arrow in arrow_group if arrow.key == key]
        if not possible_hits:
            print("No possible hits found - counting as miss")
            self.combo = 0  # Reset combo when no possible hits are found
            self.hit_type = "Miss"
            self.hit_color = (128, 128, 128)  # Gray color for misses
            self.hit_feedback = "Miss"
            self.hit_feedback_timer = pygame.time.get_ticks()
            self.score += SCORE_MISS
            self.misses += 1  # Increment miss counter
            audio_manager.play_sound('miss')  # Play miss sound
            return "Miss"

        # Find outline for this key
        outline_sprite = next((o for o in outline_group if o.key == key), None)
        if not outline_sprite:
            print(f"No outline sprite found for key '{key}' - counting as miss")
            self.combo = 0  # Reset combo when no outline is found
            self.hit_type = "Miss"
            self.hit_color = (128, 128, 128)  # Gray color for misses
            self.hit_feedback = "Miss"
            self.hit_feedback_timer = pygame.time.get_ticks()
            self.score += SCORE_MISS
            self.misses += 1  # Increment miss counter
            audio_manager.play_sound('miss')  # Play miss sound
            return "Miss"
        
        # Sort arrows by distance to outline center y
        possible_hits.sort(key=lambda a: abs(a.hitbox.centery - outline_sprite.rect.centery))
        closest_arrow = possible_hits[0]

        # Check if hitboxes overlap horizontally
        if not (closest_arrow.hitbox.right >= outline_sprite.rect.left and 
                closest_arrow.hitbox.left <= outline_sprite.rect.right):
            print("Arrow not overlapping horizontally with outline - counting as miss")
            self.combo = 0
            self.hit_type = "Miss"
            self.hit_color = (128, 128, 128)  # Gray color for misses
            self.hit_feedback = "Miss"
            self.hit_feedback_timer = pygame.time.get_ticks()
            self.score += SCORE_MISS
            self.misses += 1  # Increment miss counter
            audio_manager.play_sound('miss')  # Play miss sound
            return "Miss"

        # Calculate vertical overlap using hitboxes
        vertical_overlap = min(closest_arrow.hitbox.bottom, outline_sprite.rect.bottom) - max(closest_arrow.hitbox.top, outline_sprite.rect.top)
        if vertical_overlap <= 0:
            print("No vertical overlap between arrow and outline - counting as miss")
            self.combo = 0
            self.hit_type = "Miss"
            self.hit_color = (128, 128, 128)  # Gray color for misses
            self.hit_feedback = "Miss"
            self.hit_feedback_timer = pygame.time.get_ticks()
            self.score += SCORE_MISS
            self.misses += 1  # Increment miss counter
            audio_manager.play_sound('miss')  # Play miss sound
            return "Miss"

        # Calculate center distance and determine if hit is early or late
        center_dist = abs(closest_arrow.hitbox.centery - outline_sprite.rect.centery)
        is_late = closest_arrow.hitbox.centery > outline_sprite.rect.centery

        # Check if arrow is within the outline's vertical bounds
        is_within_outline = (closest_arrow.hitbox.bottom >= outline_sprite.rect.top and 
                            closest_arrow.hitbox.top <= outline_sprite.rect.bottom)

        # Determine hit type based on timing and position
        if center_dist <= HIT_MARGIN_PERFECT:
            base_score = SCORE_PERFECT
            self.score += self.apply_score(base_score)
            self.hit_type = "Perfect"
            self.hit_color = (0, 255, 0)  # Green
            points_earned = self.apply_score(base_score)
            self.combo += 1
            audio_manager.play_sound('perfect')  # Play perfect sound
        elif center_dist <= HIT_MARGIN_GOOD:
            base_score = SCORE_GOOD
            self.score += self.apply_score(base_score)
            self.hit_type = "Good"
            self.hit_color = (255, 255, 0)  # Yellow
            points_earned = self.apply_score(base_score)
            self.combo += 1
            audio_manager.play_sound('good')  # Play good sound
        elif is_within_outline:
            # For early/late hits, check if the arrow is within the late margin
            if center_dist <= HIT_MARGIN_LATE:
                base_score = SCORE_LATE
                self.score += self.apply_score(base_score)
                self.hit_type = "Late" if is_late else "Early"
                self.hit_color = (255, 0, 0)  # Red
                points_earned = self.apply_score(base_score)
                self.combo += 1
                audio_manager.play_sound('good')  # Play good sound for late/early hits
            else:
                print(f"Hit too far: center distance {center_dist} - counting as miss")
                self.combo = 0
                self.hit_type = "Miss"
                self.hit_color = (128, 128, 128)  # Gray color for misses
                self.hit_feedback = "Miss"
                self.hit_feedback_timer = pygame.time.get_ticks()
                self.score += SCORE_MISS
                self.misses += 1  # Increment miss counter
                audio_manager.play_sound('miss')  # Play miss sound
                return "Miss"
        else:
            print(f"Hit too far: center distance {center_dist} - counting as miss")
            self.combo = 0
            self.hit_type = "Miss"
            self.hit_color = (128, 128, 128)  # Gray color for misses
            self.hit_feedback = "Miss"
            self.hit_feedback_timer = pygame.time.get_ticks()
            self.score += SCORE_MISS
            self.misses += 1  # Increment miss counter
            audio_manager.play_sound('miss')  # Play miss sound
            return "Miss"

        # Update max combo
        self.max_combo = max(self.max_combo, self.combo)

        arrow_group.remove(closest_arrow)
        
        # Check if this is part of a combo
        current_time = pygame.time.get_ticks()
        if current_time - self.hit_feedback_timer < 100:  # 100ms window for combo hits
            self.combo_hits += 1
            self.combo_score += points_earned
            multiplier = self.get_combo_multiplier()
            self.hit_feedback = f"{self.hit_type} x{self.combo_hits} +{self.combo_score} ({multiplier}x)"
        else:
            self.combo_hits = 1
            self.combo_score = points_earned
            multiplier = self.get_combo_multiplier()
            self.hit_feedback = f"{self.hit_type} ({multiplier}x)"

        self.hit_feedback_timer = current_time
        print(f"Hit type: {self.hit_type}, Distance: {center_dist}, Is Late: {is_late}")
        return self.hit_type 