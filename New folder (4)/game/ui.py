import pygame
from .settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font = pygame.font.Font("fonts/PixelOperator8.ttf", 16)
            self.title_font = pygame.font.Font("fonts/PixelOperator8-Bold.ttf", 32)
        except pygame.error:
            print("Warning: Could not load custom fonts, using system fonts")
            self.font = pygame.font.SysFont("Arial", 16)
            self.title_font = pygame.font.SysFont("Arial", 32)
        
    def draw_text(self, text, font, color, x, y, centered=False):
        """Draw text on the screen."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if centered:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    def draw_health_bar(self, health, x, y):
        """Draw the health bar."""
        ratio = health / 100
        pygame.draw.rect(self.screen, UI_BACKGROUND_COLOR, (x - 2, y - 2, HEALTH_BAR_WIDTH + 4, HEALTH_BAR_HEIGHT + 4))
        pygame.draw.rect(self.screen, (200, 0, 0), (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        if health > 0:
            pygame.draw.rect(self.screen, (0, 200, 0), (x, y, HEALTH_BAR_WIDTH * ratio, HEALTH_BAR_HEIGHT))
            
    def draw_game_stats(self, game_state):
        """Draw game statistics (score, lives, level)."""
        # Draw score
        self.draw_text(f"Score: {game_state.score}", self.font, TEXT_COLOR, 10, 10)
        self.draw_text(f"High Score: {game_state.high_score}", self.font, TEXT_COLOR, 10, 30)
        
        # Draw lives
        self.draw_text(f"Lives: {game_state.lives}", self.font, TEXT_COLOR, 10, 50)
        
        # Draw level
        self.draw_text(f"Level: {game_state.level}", self.font, TEXT_COLOR, 10, 70)
        
    def draw_pause_menu(self):
        """Draw the pause menu."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause text
        self.draw_text("PAUSED", self.title_font, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, True)
        self.draw_text("Press ESC to resume", self.font, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, True)
        
    def draw_game_over(self, game_state):
        """Draw the game over screen."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(192)
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        if game_state.victory:
            title = "VICTORY!"
        else:
            title = "GAME OVER"
            
        self.draw_text(title, self.title_font, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, True)
        self.draw_text(f"Final Score: {game_state.score}", self.font, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, True)
        self.draw_text("Press SPACE to play again", self.font, TEXT_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, True)
        
    def draw(self, game_state):
        """Main draw method that handles all UI elements."""
        self.draw_game_stats(game_state)
        
        if game_state.is_paused:
            self.draw_pause_menu()
        elif game_state.game_over or game_state.victory:
            self.draw_game_over(game_state) 