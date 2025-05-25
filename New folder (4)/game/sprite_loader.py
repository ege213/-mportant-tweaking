import pygame

# Animation row mapping in sprite sheets
animations_map = {
    "idle": 0,
    "run": 1,
    "jump": 2,
    "fall": 2,
    "attack": 3
}

def load_sprite_sheets(filename, width, height):
    """
    Load a sprite sheet and split it into individual frames.
    Returns a dictionary of animation states with their respective frames.
    """
    try:
        sprite_sheet = pygame.image.load(filename).convert_alpha()
    except pygame.error:
        # Return a default animation if sprite sheet is missing
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        pygame.draw.rect(surface, (255, 0, 255), surface.get_rect(), 1)  # Purple outline for missing texture
        return {"idle": [surface]}
    
    sprites = {}
    sprites["idle"] = []
    
    # Just create 4 frames for idle animation as fallback
    for i in range(4):
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(i * width, 0, width, height)
        try:
            surface.blit(sprite_sheet, (0, 0), rect)
        except:
            pygame.draw.rect(surface, (255, 0, 255), surface.get_rect(), 1)
        sprites["idle"].append(surface)
            
    return sprites

def load_tile_sheet(filename, width, height):
    """
    Load a tile sheet and split it into individual tiles.
    Returns a list of tile surfaces.
    """
    try:
        tile_sheet = pygame.image.load(filename).convert_alpha()
    except pygame.error:
        # Return a default tile if tile sheet is missing
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        pygame.draw.rect(surface, (100, 100, 100), surface.get_rect())  # Gray rectangle for missing tiles
        return [surface]
    
    tiles = []
    
    sheet_width = tile_sheet.get_width() // width
    sheet_height = tile_sheet.get_height() // height
    
    for row in range(sheet_height):
        for col in range(sheet_width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(col * width, row * height, width, height)
            surface.blit(tile_sheet, (0, 0), rect)
            tiles.append(surface)
            
    return tiles 