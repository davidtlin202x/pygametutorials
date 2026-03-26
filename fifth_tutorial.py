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
isJumping = False
jumpCount = 10

# Platforms (1/3 of width, stairstep pattern)
P_WIDTH = WIDTH // 3
P_HEIGHT = 20
platforms = [
    pygame.Rect(0, HEIGHT-50, P_WIDTH, P_HEIGHT),
    pygame.Rect(WIDTH // 3, HEIGHT-200, P_WIDTH, P_HEIGHT),
    pygame.Rect(2*WIDTH // 3, HEIGHT-350, P_WIDTH, P_HEIGHT)
]
PLATFORM_COLOR = (0, 255, 0)
PLAYER_COLOR = (128, 0, 128)

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
                on_platform = any(
                    player.bottom >= p.top and player.bottom <= p.top + 10 and
                    player.right > p.left and player.left < p.right for p in platforms
                )
                if on_platform:
                    isJumping = True
                    jumpCount = 10

    # Movement L/R
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 5

    # Jumping
    if isJumping:
        if jumpCount >= -10:
            player.y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else:
            isJumping = False
    else:
        if not any(player.colliderect(p) for p in platforms):
            player.y += 5  # gravity


    # Drawing
    win.fill(BGCOLOR)
    for platform in platforms:
        pygame.draw.rect(win, PLATFORM_COLOR, platform)
    pygame.draw.rect(win, PLAYER_COLOR, player)  # player as solid rectangle

    # Keep player inside game area
    player.clamp_ip(win.get_rect())

    pygame.display.update()

pygame.quit()
