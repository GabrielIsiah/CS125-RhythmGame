import queue
import pandas as pd
from game.constants import SPAWN_WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT, ARROW_SPACING, NORMAL_HIT_ZONE_Y, GRAVITY_HIT_ZONE_Y
from Sprites.tiles import Tiles, spawn_positions
from game.pattern_manager import PatternManager
import os
import pygame
import random

class ArrowSpawner:
    def __init__(self, arrows, songs_data):
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
        self.spawning_allowed = True # Flag to control spawning
        self.songs_data = songs_data # Store the songs data
        self.last_spawn_time = 0
        self.spawn_delay = 1.0  # Base delay between spawns
        self.pattern_mode = False
        self.pattern_index = 0
        self.pattern = []
        self.timestamps = []

    def add_timestamps(self, song_key):
        # Get key log file path from SONGS dictionary
        song_info = self.songs_data.get(song_key)
        if song_info and "key_log_file" in song_info:
            key_log_path = os.path.join(song_info["key_log_file"])
        else:
            print(f"[ERROR] Key log file not found for song key: {song_key}")
            return # Stop if key log file not found

        try:
            file = pd.read_csv(key_log_path)
            for _, row in file.iterrows():
                ts = round(row['timestamp'], 3)
                self.spawn_queue.put(ts)
                # Store keys as a list for each timestamp
                self.timestamp_key_dict[ts] = row['key'].split(',') if isinstance(row['key'], str) else [row['key']]
        except FileNotFoundError:
            print(f"[ERROR] Key log file not found at: {key_log_path}")
        except KeyError as e:
            print(f"[ERROR] Missing column in key log file: {e}")
        except Exception as e:
            print(f"[ERROR] Error reading key log file: {e}")

    def get_sprite(self, key):
        return self.arrows.get(self.key_to_arrow.get(key))

    def start_pattern_mode(self, difficulty):
        self.use_patterns = True
        self.difficulty = difficulty
        self.pattern_manager.difficulty = difficulty

    def stop_pattern_mode(self):
        if self.use_patterns:
            self.use_patterns = False

    def spawn_arrow(self, current_time, arrow_group, gravity_mode=False):
        """Spawn a new arrow based on the current game mode and time."""
        if not self.spawning_allowed:
            return

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
                        if gravity_mode:
                            tile.rect.bottom = WINDOW_HEIGHT + 100
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
                    if gravity_mode:
                        tile.rect.bottom = WINDOW_HEIGHT + 100
                    arrow_group.add(tile)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, key):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.key = key 