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

# All difficulties use the same speed
DIFFICULTY_SPEEDS = {
    "easy": BASE_ARROW_SPEED,      
    "medium": BASE_ARROW_SPEED,    
    "hard": BASE_ARROW_SPEED 
}

# Spawn settings
SPAWN_WINDOW = 1.55
MUSIC_START_DELAY = 5.0
VIDEO_START_DELAY = 4.4

# Arrow and outline spacing
ARROW_SPACING = 200  # Space between arrows horizontally
OUTLINE_SPACING = 200  # Space between outlines horizontally

# Gravity mode settings (for medium difficulty)
GRAVITY_MIN_DURATION = 15.0  # Minimum duration of gravity mode in seconds
GRAVITY_MAX_DURATION = 25.0  # Maximum duration of gravity mode in seconds
GRAVITY_NORMAL_MIN_DURATION = 20.0  # Minimum duration of normal mode in seconds
GRAVITY_NORMAL_MAX_DURATION = 30.0  # Maximum duration of normal mode in seconds
GRAVITY_SAFE_INTERVAL = 2.0  # Minimum time between arrows for safe gravity switch

# UI Positions
SCORE_POSITION = (50, 50)  # Moved to upper left
MISS_POSITION = (50, 100)  # Below score
COMBO_POSITION = (50, 150)  # Below misses
FEEDBACK_POSITION = (WINDOW_WIDTH // 2, 200)  # Centered horizontally

# Hit zone positions (symmetric relative to screen edges)
HIT_ZONE_EDGE_DISTANCE = 150  # Distance from screen edge to hit zone
NORMAL_HIT_ZONE_Y = WINDOW_HEIGHT - HIT_ZONE_EDGE_DISTANCE  # Bottom hit zone (750)
GRAVITY_HIT_ZONE_Y = HIT_ZONE_EDGE_DISTANCE  # Top hit zone (150) 