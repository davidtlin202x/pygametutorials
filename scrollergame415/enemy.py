import pygame

ENEMY_COLOR = (200, 50, 75)
ENEMY_SPEED = 2
ENEMY_SIZE = 35

class Enemy:

    def __init__(self, platform, offset=0):
        self.platform = platform
        self.rect = pygame.Rect(
            platform.rect.x + offset,
            platform.rect.y - ENEMY_SIZE,
            ENEMY_SIZE, ENEMY_SIZE
        )
        self.direction = 1
    
    def movement(self):
        self.rect.x += ENEMY_SPEED * self.direction
        if self.rect.left <= self.platform.rect.left:
            self.direction = 1
        elif self.rect.right >= self.platform.rect.right:
            self.direction = -1
    
    def draw(self, win, camera_x):
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(win, ENEMY_COLOR, draw_rect)
    
    def check_player_collision(self, player):
        return self.rect.colliderect(player)
