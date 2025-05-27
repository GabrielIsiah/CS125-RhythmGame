# Game window settings
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
FPS = 60

# Hit detection margins
HIT_MARGIN_PERFECT = 20
HIT_MARGIN_GOOD = 65
HIT_MARGIN_LATE = 100

# Scoring system
SCORE_PERFECT = 100
SCORE_GOOD = 50
SCORE_LATE = 25
SCORE_MISS = 0  # No points for misses, just resets combo

# Feedback display
HIT_FEEDBACK_DURATION = 500  # milliseconds

# Base game speed (for easy difficulty)
# Distance: 850 pixels (from y=1600 to y=750)
# Target time: 1.5 seconds
# Required speed: 850 pixels / 1.5 seconds = 566.67 pixels/second
# At 60 FPS: 566.67/60 ≈ 9.44 pixels per frame
BASE_ARROW_SPEED = 9.44

# Difficulty speed multipliers
DIFFICULTY_SPEEDS = {
    "easy": BASE_ARROW_SPEED,      # Base speed
    "medium": BASE_ARROW_SPEED * 1.2,  # 20% faster
    "hard": BASE_ARROW_SPEED * 1.4   # 40% faster
}

# Spawn settings
SPAWN_WINDOW = 1.55
MUSIC_START_DELAY = 5.0  # seconds 