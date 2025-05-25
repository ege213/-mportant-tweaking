import pygame
import os
from .settings import MUSIC_VOLUME, SFX_VOLUME

class SoundManager:
    def __init__(self):
        self.sounds = {}
        sound_files = {
            "jump": "sounds/jump.wav",
            "coin": "sounds/coin.wav",
            "power_up": "sounds/power_up.wav",
            "hurt": "sounds/hurt.wav",
            "explosion": "sounds/explosion.wav",
            "tap": "sounds/tap.wav"
        }
        
        # Load available sound effects
        for name, path in sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
                self.sounds[name].set_volume(SFX_VOLUME)
            except pygame.error:
                print(f"Warning: Could not load sound file: {path}")
                
        # Try to load background music
        try:
            pygame.mixer.music.load("music/time_for_adventure.mp3")
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            self.has_music = True
        except pygame.error:
            print("Warning: Could not load background music")
            self.has_music = False
            
    def play_sound(self, sound_name):
        """Play a sound effect by name."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            
    def play_music(self):
        """Start playing background music on loop."""
        if self.has_music:
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        
    def stop_music(self):
        """Stop the background music."""
        if self.has_music:
            pygame.mixer.music.stop()
        
    def pause_music(self):
        """Pause the background music."""
        if self.has_music:
            pygame.mixer.music.pause()
        
    def unpause_music(self):
        """Unpause the background music."""
        if self.has_music:
            pygame.mixer.music.unpause()
        
    def set_music_volume(self, volume):
        """Set the volume of the background music (0.0 to 1.0)."""
        if self.has_music:
            pygame.mixer.music.set_volume(volume)
        
    def set_sfx_volume(self, volume):
        """Set the volume of all sound effects (0.0 to 1.0)."""
        for sound in self.sounds.values():
            sound.set_volume(volume) 