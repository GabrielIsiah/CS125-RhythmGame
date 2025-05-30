import queue
import threading
import random
import time
from typing import List, Dict, Optional

class Pattern:
    def __init__(self, keys: List[str], timing: float, difficulty: str):
        self.keys = keys  # List of keys to press
        self.timing = timing  # Timing between arrows
        self.difficulty = difficulty  # Difficulty level

class PatternManager:
    def __init__(self):
        self.pattern_queue = queue.Queue()
        self.current_pattern: Optional[Pattern] = None
        self.pattern_thread: Optional[threading.Thread] = None
        self.is_running = False
        # Pattern pools and weights for each difficulty
        self.pattern_pools = {
            'easy': (
                [ ['d'], ['f'], ['j'], ['k'], ['f','j'], ['d','k'], ['d','f','j'], ['d','f','j','k'] ],
                [0.2, 0.2, 0.2, 0.2, 0.08, 0.08, 0.01, 0.01]
            ),
            'medium': (
                [ ['d'], ['f'], ['j'], ['k'], ['d','f'], ['j','k'], ['d','f','j'], ['f','j','k'], ['d','f','j','k'] ],
                [0.18, 0.18, 0.18, 0.18, 0.09, 0.09, 0.04, 0.04, 0.02 ]
            ),
            'hard': (
                [ ['d'], ['f'], ['j'], ['k'], ['d','f'], ['j','k'], ['d','f','j'], ['f','j','k'], ['d','f','j','k'], ['d','d','f','f'], ['j','j','k','k'] ],
                [0.12, 0.12, 0.12, 0.12, 0.10, 0.10, 0.08, 0.08, 0.06, 0.05, 0.05 ]
            )
        }

    def get_weighted_pattern(self, difficulty: str) -> List[str]:
        pool, weights = self.pattern_pools.get(difficulty, self.pattern_pools['easy'])
        return random.choices(pool, weights=weights, k=1)[0]

    def generate_patterns(self, difficulty: str) -> List[Pattern]:
        # (keep for legacy/multithreaded use if needed)
        patterns = {
            'easy': [
                Pattern(['d'], 1.0, 'easy'),
                Pattern(['f'], 1.0, 'easy'),
                Pattern(['j'], 1.0, 'easy'),
                Pattern(['k'], 1.0, 'easy'),
                Pattern(['d', 'f'], 0.8, 'easy'),
                Pattern(['j', 'k'], 0.8, 'easy')
            ]
        }
        return patterns.get(difficulty, patterns['easy'])

    def start_pattern_generation(self, difficulty: str) -> None:
        self.is_running = True
        self.pattern_thread = threading.Thread(
            target=self._pattern_generation_loop,
            args=(difficulty,),
            daemon=True  # Make thread daemon so it exits when main program exits
        )
        self.pattern_thread.start()

    def _pattern_generation_loop(self, difficulty: str) -> None:
        patterns = self.generate_patterns(difficulty)
        while self.is_running:
            pattern = random.choice(patterns)
            self.pattern_queue.put(pattern)
            time.sleep(pattern.timing)

    def get_next_pattern(self) -> Optional[Pattern]:
        if not self.pattern_queue.empty():
            return self.pattern_queue.get()
        return None

    def stop(self) -> None:
        self.is_running = False
        if self.pattern_thread and self.pattern_thread.is_alive():
            self.pattern_thread.join(timeout=1.0)  # Wait up to 1 second for thread to finish 