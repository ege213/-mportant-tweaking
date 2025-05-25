import pygame
from .settings import *
from .player import Player
from .sprite_loader import load_tile_sheet
from .entities import Platform, Coin, Fruit, Slime, Spike
from .level_data import *

class Level:
    def __init__(self, sound_manager, level_number=1):
        self.sound_manager = sound_manager
        self.display_surface = pygame.display.get_surface()
        self.level_number = level_number
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        
        # Load tiles
        self.tiles = load_tile_sheet("sprites/world_tileset.png", TILE_SIZE, TILE_SIZE)
        
        # Set up the level
        self.setup_level()
        
        # Start background music
        self.sound_manager.play_music()
        
    def setup_level(self):
        """Set up the level layout from the tile map."""
        level_data = LEVELS.get(self.level_number, LEVELS[1])  # Default to level 1 if not found
        
        # Clear existing sprites
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.collectibles.empty()
        self.hazards.empty()
        
        # Create level from tile map
        for row_index, row in enumerate(level_data):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if cell == GROUND or cell == PLATFORM:
                    platform = Platform(x, y, TILE_SIZE, TILE_SIZE)
                    self.platforms.add(platform)
                    self.all_sprites.add(platform)
                    
                elif cell == COIN:
                    coin = Coin(x, y)
                    self.collectibles.add(coin)
                    self.all_sprites.add(coin)
                    
                elif cell == FRUIT:
                    fruit = Fruit(x, y)
                    self.collectibles.add(fruit)
                    self.all_sprites.add(fruit)
                    
                elif cell == SLIME:
                    slime = Slime(x, y, "purple")
                    self.enemies.add(slime)
                    self.all_sprites.add(slime)
                    
                elif cell == SPIKE:
                    spike = Spike(x, y)
                    self.hazards.add(spike)
                    self.all_sprites.add(spike)
                    
                elif cell == START:
                    # Create player at start position
                    self.player = Player(x, y, self.sound_manager)
                    self.all_sprites.add(self.player)
        
    def create_platform(self, x, y, width, height):
        """Create a platform with the given dimensions."""
        platform = Platform(x, y, width, height)
        self.platforms.add(platform)
        self.all_sprites.add(platform)
        
    def handle_collisions(self):
        """Handle all collision detection and response."""
        # Player-Platform collisions
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for platform in hits:
            self.player.handle_collision(platform)
            
        # Player-Collectible collisions
        hits = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        for collectible in hits:
            if isinstance(collectible, Coin):
                self.player.collect_coin()
            elif isinstance(collectible, Fruit):
                self.player.collect_fruit()
                
        # Player-Enemy collisions
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits and not self.player.invincible:
            self.player.take_damage(SLIME_DAMAGE)
            
        # Player-Hazard collisions
        hits = pygame.sprite.spritecollide(self.player, self.hazards, False)
        if hits and not self.player.invincible:
            self.player.take_damage(SPIKE_DAMAGE)
            
    def update(self):
        """Update all game objects."""
        self.all_sprites.update()
        self.handle_collisions()
        
    def draw(self, screen):
        """Draw all game objects."""
        screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(screen)
        
    def handle_event(self, event):
        """Handle game events."""
        pass
        
    def next_level(self):
        """Advance to the next level."""
        self.level_number += 1
        if self.level_number in LEVELS:
            self.setup_level()
            return True
        return False  # No more levels 