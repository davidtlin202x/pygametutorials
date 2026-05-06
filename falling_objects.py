import pygame
import random
import math

pygame.init()
sc = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

# Player (circle)
player_x = 200
player_y = 550
player_radius = 20
player_speed = 5

# Create 4 enemies (rectangles)
enemies = []
for i in range(4):
    enemy = pygame.Rect(random.randint(0, 360), random.randint(-600, 0), 40, 40)
    enemies.append(enemy)

score = 0
font = pygame.font.SysFont(None, 36)

# Circle-rectangle collision function
def circle_rect_collision(circle_x, circle_y, radius, rect):
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))

    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y

    return (distance_x ** 2 + distance_y ** 2) <= radius ** 2

running = True

while running:
    sc.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Keep player inside screen
    if player_x - player_radius < 0:
        player_x = player_radius
    if player_x + player_radius > 400:
        player_x = 400 - player_radius

    for enemy in enemies:
        enemy.y += random.randint(2, 6)

        if enemy.y > 600:
            enemy.y = 0
            enemy.x = random.randint(0, 360)
            score += 1

        if circle_rect_collision(player_x, player_y, player_radius, enemy):
            running = False

        pygame.draw.rect(sc, (255, 0, 0), enemy)

    pygame.draw.circle(sc, (0, 255, 0), (player_x, player_y), player_radius)

    text = font.render("Score: " + str(score), True, (255, 255, 255))
    sc.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
