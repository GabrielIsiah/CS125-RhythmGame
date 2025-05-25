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

    def check_miss(self, arrow):
        """Handle missed arrows that pass the hit zone"""
        self.combo = 0  # Reset combo on miss
        self.hit_type = "Miss"
        self.hit_color = (128, 128, 128)  # Gray color for misses
        self.hit_feedback = "Miss"
        self.hit_feedback_timer = pygame.time.get_ticks()
        self.score += SCORE_MISS
        return True

    def check_hit(self, key, arrow_group, outline_group):
        print(f"Checking hits for key '{key}'")

        possible_hits = [arrow for arrow in arrow_group if arrow.key == key]
        if not possible_hits:
            print("No possible hits found")
            return None

        # Find outline for this key
        outline_sprite = next((o for o in outline_group if o.key == key), None)
        if not outline_sprite:
            print(f"No outline sprite found for key '{key}'")
            return None
        
        # Sort arrows by distance to outline center y
        possible_hits.sort(key=lambda a: abs(a.hitbox.centery - outline_sprite.rect.centery))
        closest_arrow = possible_hits[0]

        # Check if hitboxes overlap horizontally
        if not (closest_arrow.hitbox.right >= outline_sprite.rect.left and 
                closest_arrow.hitbox.left <= outline_sprite.rect.right):
            print("Arrow not overlapping horizontally with outline")
            return None

        # Calculate vertical overlap using hitboxes
        vertical_overlap = min(closest_arrow.hitbox.bottom, outline_sprite.rect.bottom) - max(closest_arrow.hitbox.top, outline_sprite.rect.top)
        if vertical_overlap <= 0:
            print("No vertical overlap between arrow and outline")
            return None

        # Calculate center distance and determine if hit is early or late
        center_dist = abs(closest_arrow.hitbox.centery - outline_sprite.rect.centery)
        is_late = closest_arrow.hitbox.centery > outline_sprite.rect.centery

        # Check if arrow is within the outline's vertical bounds
        is_within_outline = (closest_arrow.hitbox.bottom >= outline_sprite.rect.top and 
                            closest_arrow.hitbox.top <= outline_sprite.rect.bottom)

        # Determine hit type based on timing and position
        if center_dist <= HIT_MARGIN_PERFECT:
            self.score += SCORE_PERFECT
            self.hit_type = "Perfect"
            self.hit_color = (0, 255, 0)  # Green
            points_earned = SCORE_PERFECT
            self.combo += 1
        elif center_dist <= HIT_MARGIN_GOOD:
            self.score += SCORE_GOOD
            self.hit_type = "Good"
            self.hit_color = (255, 255, 0)  # Yellow
            points_earned = SCORE_GOOD
            self.combo += 1
        elif is_within_outline:
            # For early/late hits, check if the arrow is within the late margin
            if center_dist <= HIT_MARGIN_LATE:
                self.score += SCORE_LATE
                self.hit_type = "Late" if is_late else "Early"
                self.hit_color = (255, 0, 0)  # Red
                points_earned = SCORE_LATE
                self.combo += 1
            else:
                print(f"Hit too far: center distance {center_dist}")
                return None
        else:
            print(f"Hit too far: center distance {center_dist}")
            return None

        # Update max combo
        self.max_combo = max(self.max_combo, self.combo)

        arrow_group.remove(closest_arrow)
        
        # Check if this is part of a combo
        current_time = pygame.time.get_ticks()
        if current_time - self.hit_feedback_timer < 100:  # 100ms window for combo hits
            self.combo_hits += 1
            self.combo_score += points_earned
            self.hit_feedback = f"{self.hit_type} x{self.combo_hits} +{self.combo_score}"
        else:
            self.combo_hits = 1
            self.combo_score = points_earned
            self.hit_feedback = self.hit_type

        self.hit_feedback_timer = current_time
        print(f"Hit type: {self.hit_type}, Distance: {center_dist}, Is Late: {is_late}")
        return self.hit_type 