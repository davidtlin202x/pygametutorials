import pygame

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 72)

# --- Constants ---
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
MOVE_SPEED = 5
GRAVITY = 5
JUMP_POWER = 10

BGCOLOR = (255,255,255)
PLAYER_COLOR = (128,0,128)
PLATFORM_COLOR = (0,255,0)

# --- Window ---
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Jump Game")

# --- Player ---
player = pygame.Rect(50, HEIGHT-100, PLAYER_SIZE, PLAYER_SIZE)
is_jumping = False
jump_count = JUMP_POWER

# --- Platforms ---
P_WIDTH, P_HEIGHT = WIDTH//3, 20
platforms = [
    pygame.Rect(0, HEIGHT-50, P_WIDTH, P_HEIGHT),
    pygame.Rect(WIDTH//3, HEIGHT-200, P_WIDTH, P_HEIGHT),
    pygame.Rect(2*WIDTH//3, HEIGHT-350, P_WIDTH, P_HEIGHT)
]

running, game_over = True, False

# --- Game Loop ---
while running:
    clock.tick(30)

    # Events
    for e in pygame.event.get():
        if game_over:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    # Reset game state
                    game_over = False
                    player.topleft = (50, HEIGHT-100)
                    is_jumping = False
                    JUMP_POWER = 10
                    MOVE_SPEED = 5
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                running = False
            if e.key == pygame.K_SPACE:
                on_platform = any(
                    player.bottom in range(p.top, p.top+10) and
                    player.right > p.left and player.left < p.right
                    for p in platforms
                )
                if on_platform:
                    is_jumping = True
                    jump_count = JUMP_POWER

    # Movement
    keys = pygame.key.get_pressed()
    player.x += (keys[pygame.K_d] or keys[pygame.K_RIGHT]) * MOVE_SPEED
    player.x -= (keys[pygame.K_a] or keys[pygame.K_LEFT]) * MOVE_SPEED

    # Jump / Gravity
    if is_jumping:
        if jump_count >= -JUMP_POWER:
            player.y -= (jump_count * abs(jump_count)) * 0.5
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = JUMP_POWER
    else:
        if not any(player.colliderect(p) for p in platforms):
            player.y += GRAVITY

    # Platform snap
    for p in platforms:
        if player.colliderect(p) and player.bottom > p.top:
            player.bottom = p.top
            is_jumping = False
            jump_count = JUMP_POWER

    # Boundaries
    player.clamp_ip(win.get_rect())
    if player.bottom >= HEIGHT:
        game_over = True

    # Draw
    win.fill(BGCOLOR)
    for p in platforms:
        pygame.draw.rect(win, PLATFORM_COLOR, p)
    pygame.draw.rect(win, PLAYER_COLOR, player)

    if game_over:
        txt1 = font.render("YOU LOSE!", True, (255,0,0))
        txt2 = font.render("Press R to Restart", True, (0,0,255))
        win.blit(txt1, txt1.get_rect(center=(WIDTH//2, HEIGHT//2-25)))
        win.blit(txt2, txt2.get_rect(center=(WIDTH//2, HEIGHT//2+25)))
        jump_count = 0
        MOVE_SPEED = 0

    pygame.display.update()

pygame.quit()
