import pygame

pygame.init()
clock = pygame.time.Clock()

# Window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Jump Game")
BGCOLOR = (255, 255, 255)

# Player
player_width, player_height = 40, 40
x_pos = 50
y_pos = HEIGHT - 100  # start above ground
player = pygame.Rect(x_pos, y_pos, player_width, player_height)

# Jumping
#TO DO

# Platforms (1/3 of width, stairstep pattern)
# TO DO

running = True
while running:
    clock.tick(30)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_SPACE:
                # Jump only if standing on a platform
                # To do

    # Movement L/R
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 5

    # Jumping
    TO DO


    # Drawing
    win.fill(BGCOLOR)
    for platform in platforms:
        pygame.draw.rect(win, PLATFORM_COLOR, platform)
    pygame.draw.rect(win, PLAYER_COLOR, player)  # player as solid rectangle

    # Keep player inside game area
    player.clamp_ip(win.get_rect())

    pygame.display.update()

pygame.quit()
