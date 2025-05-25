import pygame
from .settings import *
from .sprite_loader import load_sprite_sheets

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Load platform tiles
        tiles = load_sprite_sheets("sprites/platforms.png", TILE_SIZE, TILE_SIZE)
        if "idle" in tiles and tiles["idle"]:
            tile = tiles["idle"][0]
            # Tile the platform with the graphic
            for tile_x in range(0, width, TILE_SIZE):
                for tile_y in range(0, height, TILE_SIZE):
                    self.image.blit(tile, (tile_x, tile_y))
        else:
            # Fallback to a colored rectangle if sprite not found
            self.image.fill((100, 100, 100))
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = load_sprite_sheets("sprites/coin.png", TILE_SIZE, TILE_SIZE)
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        # Animate the coin
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites["idle"]):
            self.current_sprite = 0
        self.image = self.sprites["idle"][int(self.current_sprite)]

class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = load_sprite_sheets("sprites/fruit.png", TILE_SIZE, TILE_SIZE)
        self.current_sprite = 0
        self.animation_speed = 0.15
        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        # Animate the fruit
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites["idle"]):
            self.current_sprite = 0
        self.image = self.sprites["idle"][int(self.current_sprite)]

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        sprite_file = f"sprites/slime_{color}.png"
        self.sprites = load_sprite_sheets(sprite_file, TILE_SIZE, TILE_SIZE)
        self.current_sprite = 0
        self.animation_speed = 0.15
        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement
        self.direction = pygame.math.Vector2(1, 0)
        self.speed = SLIME_SPEED
        self.move_distance = 100
        self.start_x = x
        
    def update(self):
        # Move the slime back and forth
        self.rect.x += self.direction.x * self.speed
        
        # Check if we need to turn around
        if abs(self.rect.x - self.start_x) > self.move_distance:
            self.direction.x *= -1
            
        # Animate the slime
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites["idle"]):
            self.current_sprite = 0
        self.image = self.sprites["idle"][int(self.current_sprite)]
        
        # Flip sprite based on direction
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = load_sprite_sheets("sprites/spike.png", TILE_SIZE, TILE_SIZE)
        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 