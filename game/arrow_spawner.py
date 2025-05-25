import queue
import pandas as pd
from game.constants import SPAWN_WINDOW
from Sprites.tiles import Tiles, spawn_positions

class ArrowSpawner:
    def __init__(self, arrows):
        self.spawn_queue = queue.Queue()
        self.timestamp_key_dict = {}
        self.arrows = arrows

    def add_timestamps(self):
        file = pd.read_csv('key_log.csv')
        for _, row in file.iterrows():
            ts = round(row['timestamp'], 3)
            self.spawn_queue.put(ts)
            # Store keys as a list for each timestamp
            self.timestamp_key_dict[ts] = row['key'].split(',') if isinstance(row['key'], str) else [row['key']]

    def get_sprite(self, key):
        match key:
            case 'd':
                return self.arrows['left_arrow']
            case 'f':
                return self.arrows['down_arrow']
            case 'j':
                return self.arrows['up_arrow']
            case 'k':
                return self.arrows['right_arrow']
            case _:
                return None

    def spawn_arrow(self, current_time, arrow_group):
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