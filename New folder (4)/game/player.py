import pygame
from .settings import *
from .sprite_loader import load_sprite_sheets

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sound_manager):
        super().__init__()
        self.sound_manager = sound_manager
        
        # Load sprite sheets
        self.sprites = load_sprite_sheets("sprites/knight.png", 32, 32)
        self.current_sprite = 0
        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement variables
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.acceleration = PLAYER_ACCELERATION
        self.friction = PLAYER_FRICTION
        self.gravity = PLAYER_GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED
        self.jumping = False
        self.facing_right = True
        
        # Animation variables
        self.current_animation = "idle"
        self.animation_index = 0
        self.animation_speed = PLAYER_ANIMATION_SPEED
        self.animation_time = 0
        
        # Game state
        self.health = 100
        self.score = 0
        self.invincible = False
        self.invincible_timer = 0

    def update(self):
        self.apply_gravity()
        self.handle_movement()
        self.animate()
        self.update_invincibility()

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0
            
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and not self.jumping:
            self.jump()
            
        # Apply movement
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jumping = True
        self.sound_manager.play_sound("jump")

    def apply_gravity(self):
        self.direction.y += self.gravity
        if self.direction.y > 10:  # Terminal velocity
            self.direction.y = 10

    def animate(self):
        self.animation_time += self.animation_speed
        
        # Determine animation state
        if self.direction.y < 0 and "jump" in self.sprites:
            animation = "jump"
        elif self.direction.y > 1 and "fall" in self.sprites:
            animation = "fall"
        elif self.direction.x != 0 and "run" in self.sprites:
            animation = "run"
        else:
            animation = "idle"
            
        # If the animation doesn't exist, fall back to idle
        if animation not in self.sprites:
            animation = "idle"
            
        if animation != self.current_animation:
            self.current_animation = animation
            self.animation_index = 0
            self.animation_time = 0
            
        # Update animation frame
        sprite_list = self.sprites[self.current_animation]
        if self.animation_time >= 1:
            self.animation_time = 0
            self.animation_index = (self.animation_index + 1) % len(sprite_list)
            
        self.image = sprite_list[self.animation_index]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def handle_collision(self, sprite):
        # Handle collision with different types of sprites
        from .entities import Platform  # Import here to avoid circular import
        if isinstance(sprite, Platform):
            if self.direction.y > 0:  # Landing on platform
                self.rect.bottom = sprite.rect.top
                self.direction.y = 0
                self.jumping = False
            elif self.direction.y < 0:  # Hitting platform from below
                self.rect.top = sprite.rect.bottom
                self.direction.y = 0
        
    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()
            self.sound_manager.play_sound("hurt")
            
    def update_invincibility(self):
        if self.invincible:
            if pygame.time.get_ticks() - self.invincible_timer > 1000:  # 1 second of invincibility
                self.invincible = False
                
    def collect_coin(self):
        self.score += COIN_VALUE
        self.sound_manager.play_sound("coin")
        
    def collect_fruit(self):
        self.health = min(100, self.health + FRUIT_HEALTH_RESTORE)
        self.sound_manager.play_sound("power_up") 