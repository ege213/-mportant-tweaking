import pygame
import sys
from game.game_state import GameState
from game.settings import *
from game.player import Player
from game.level import Level
from game.sound_manager import SoundManager
from game.ui import UI

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Knight's Adventure")
        
        # Clock for controlling frame rate
    
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.sound_manager = SoundManager()
        self.game_state = GameState()
        self.level = Level(self.sound_manager)
        self.ui = UI(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state.is_paused:
                        self.game_state.unpause()
                    else:
                        self.game_state.pause()
                        
            self.level.handle_event(event)
        return True

    def update(self):
        if not self.game_state.is_paused:
            self.level.update()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.level.draw(self.screen)
        self.ui.draw(self.game_state)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 