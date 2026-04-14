import pygame

# --- Constants ---
PLATFORM_COLOR = (0, 255, 0)

class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface, camera_x):
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(surface, PLATFORM_COLOR, draw_rect)
    
    def check_collision(self, player_rect):
        """ Returns true if the player is colliding with this platform. """
        return player_rect.colliderect(self.rect)
    
    def snap_to_top(self, player_rect):
        """Return true if the player is colliding with the platform from above"""
        if player_rect.colliderect(self.rect) and player_rect.bottom > self.rect.top:
            player_rect.bottom = self.rect.top
            return True
        return False
