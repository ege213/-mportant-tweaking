class GameState:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.level = 1
        self.is_paused = False
        self.game_over = False
        self.victory = False
        
    def reset(self):
        """Reset the game state for a new game."""
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.lives = 3
        self.level = 1
        self.is_paused = False
        self.game_over = False
        self.victory = False
        
    def pause(self):
        """Pause the game."""
        self.is_paused = True
        
    def unpause(self):
        """Unpause the game."""
        self.is_paused = False
        
    def add_score(self, points):
        """Add points to the score."""
        self.score += points
        
    def lose_life(self):
        """Lose a life and check for game over."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            
    def next_level(self):
        """Advance to the next level."""
        self.level += 1
        
    def complete_game(self):
        """Mark the game as completed."""
        self.victory = True
        if self.score > self.high_score:
            self.high_score = self.score 