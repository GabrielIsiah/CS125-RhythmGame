import pygame
import os
import threading
from queue import Queue

class AudioManager:
    def __init__(self):
        # Initialize pygame mixer with multiple channels
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(8)  # Allow multiple sounds to play simultaneously
        
        # Create a queue for sound effects
        self.sound_queue = Queue()
        
        # Set default volumes
        self.sound_volume = 0.3  # 30% volume for sound effects
        self.music_volume = 0.3  # 30% volume for music (reverted to original)
        
        # Load sound effects
        self.sounds = {
            'perfect': self._load_sound('perfect.wav'),
            'good': self._load_sound('good.wav'),
            'miss': self._load_sound('miss.wav')
        }
        
        # Set volume for all sound effects
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.sound_volume)
        
        # Start the sound effect thread
        self.running = True
        self.sound_thread = threading.Thread(target=self._process_sound_queue)
        self.sound_thread.daemon = True
        self.sound_thread.start()
    
    def _load_sound(self, filename):
        """Load a sound effect from the assets/sounds directory."""
        try:
            sound_path = os.path.join('assets', 'sounds', filename)
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(self.sound_volume)
            return sound
        except Exception as e:
            print(f"Error loading sound {filename}: {e}")
            return None
    
    def _process_sound_queue(self):
        """Process the sound effect queue in a separate thread."""
        while self.running:
            try:
                sound_name = self.sound_queue.get(timeout=0.1)
                if sound_name in self.sounds and self.sounds[sound_name]:
                    self.sounds[sound_name].play()
            except:
                continue
    
    def play_sound(self, sound_name):
        """Add a sound to the queue to be played."""
        if sound_name in self.sounds:
            self.sound_queue.put(sound_name)
    
    def play_music(self, music_path, volume=None):
        """Play background music."""
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume if volume is not None else self.music_volume)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop_music(self):
        """Stop the background music."""
        pygame.mixer.music.stop()
    
    def pause_music(self):
        """Pause the background music."""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause the background music."""
        pygame.mixer.music.unpause()
    
    def cleanup(self):
        """Clean up resources."""
        self.running = False
        if self.sound_thread.is_alive():
            self.sound_thread.join(timeout=1.0)
        pygame.mixer.quit()

# Create a global instance
audio_manager = AudioManager() 