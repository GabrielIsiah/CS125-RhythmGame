import queue
import pandas as pd
from game.constants import SPAWN_WINDOW
from Sprites.tiles import Tiles, spawn_positions
from game.pattern_manager import PatternManager

class ArrowSpawner:
    def __init__(self, arrows):
        self.spawn_queue = queue.Queue()
        self.timestamp_key_dict = {}
        self.arrows = arrows
        self.key_to_arrow = {
            'd': 'left_arrow',
            'f': 'down_arrow',
            'j': 'up_arrow',
            'k': 'right_arrow'
        }
        self.pattern_manager = PatternManager()
        self.use_patterns = False  # Flag to determine if we're using patterns or CSV
        self.difficulty = 'easy'  # Default, will be set in pattern mode

    def add_timestamps(self):
        file = pd.read_csv('key_log.csv')
        for _, row in file.iterrows():
            ts = round(row['timestamp'], 3)
            self.spawn_queue.put(ts)
            # Store keys as a list for each timestamp
            self.timestamp_key_dict[ts] = row['key'].split(',') if isinstance(row['key'], str) else [row['key']]

    def get_sprite(self, key):
        return self.arrows.get(self.key_to_arrow.get(key))

    def start_pattern_mode(self, difficulty):
        self.use_patterns = True
        self.difficulty = difficulty
        self.pattern_manager.difficulty = difficulty
        # Use key log for timing, but pattern manager for pattern selection
        self.add_timestamps()

    def stop_pattern_mode(self):
        if self.use_patterns:
            self.use_patterns = False

    def spawn_arrow(self, current_time, arrow_group):
        if self.use_patterns:
            # Use key log timestamps for timing, but select pattern for each
            if not self.spawn_queue.empty():
                item = self.spawn_queue.queue[0]
                if 0 <= item - current_time <= SPAWN_WINDOW:
                    timestamp = round(self.spawn_queue.get(), 3)
                    # Instead of using the original key, select a pattern
                    pattern_keys = self.pattern_manager.get_weighted_pattern(self.difficulty)
                    for key in pattern_keys:
                        tile_img = self.get_sprite(key)
                        if tile_img is None:
                            print(f"[ERROR] No sprite found for key: '{key}'")
                            continue
                        tile = Tiles(tile_img, spawn_positions[key], key)
                        arrow_group.add(tile)
            return

        # Original CSV-based spawning logic
        if not self.spawn_queue.empty():
            item = self.spawn_queue.queue[0]
            if 0 <= item - current_time <= SPAWN_WINDOW:
                timestamp = round(self.spawn_queue.get(), 3)
                keys = self.timestamp_key_dict.get(timestamp)

                if not keys:
                    print(f"[ERROR] No keys found for timestamp: {timestamp}")
                    return

                # Process each key in the list
                for key in keys:
                    key = key.strip()  # Remove any whitespace
                    if key not in spawn_positions:
                        print(f"[ERROR] No spawn position for key: '{key}'")
                        continue

                    tile_img = self.get_sprite(key)
                    if tile_img is None:
                        print(f"[ERROR] No sprite found for key: '{key}'")
                        continue

                    tile = Tiles(tile_img, spawn_positions[key], key)
                    arrow_group.add(tile) 