import pygame
from platforms import Platform

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# --- Constants ---
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
MOVE_SPEED = 5
GRAVITY = 5
JUMP_POWER = 10

BGCOLOR = (255, 255, 255)
PLAYER_COLOR = (128, 0, 128)
COIN_COLOR = (255, 215, 0)
EXIT_COLOR = (0, 0, 0)

# --- Window ---
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Jump Game")
LEVEL_WIDTH = 2000

# --- Player ---
player = pygame.Rect(50, HEIGHT - 100, PLAYER_SIZE, PLAYER_SIZE)
is_jumping = False
jump_count = JUMP_POWER

# --- Camera ---
camera_x = 0

# --- Platforms (using Platform class) ---
platforms = [
    Platform(0, HEIGHT - 50, WIDTH // 3, 20),
    Platform(WIDTH // 3, HEIGHT - 200, WIDTH // 3, 20),
    Platform(2 * WIDTH // 3, HEIGHT - 350, WIDTH // 3, 20),
    Platform(WIDTH, HEIGHT - 259, WIDTH // 3, 20),
    Platform(WIDTH + WIDTH // 3, HEIGHT - 120, WIDTH // 3, 20)
]

# --- Coins ---
# TODO

# --- Exit ---
# TODO

# --- Game State ---
running, game_over = True, False

# --- Game Loop ---
while running:
    clock.tick(30)

    # --- Events ---
    for e in pygame.event.get():
        if game_over:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                # Reset game state
                game_over = False
                player.topleft = (50, HEIGHT - 100)
                is_jumping = False
                jump_count = JUMP_POWER
                MOVE_SPEED = 5
                coins_collected = 0
                # Create Coins
                coins = [
                    pygame.Rect(150, HEIGHT - 100, COIN_SIZE, COIN_SIZE),
                    pygame.Rect(350, HEIGHT - 250, COIN_SIZE, COIN_SIZE),
                    pygame.Rect(550, HEIGHT - 400, COIN_SIZE, COIN_SIZE),
                ]
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_q):
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            # Check if player is on a platform
            on_platform = any(player.bottom in range(p.rect.top, p.rect.top + 10) and
                              player.right > p.rect.left and player.left < p.rect.right
                              for p in platforms)
            if on_platform:
                is_jumping = True
                jump_count = JUMP_POWER

    # --- Movement ---
    keys = pygame.key.get_pressed()
    player.x += (keys[pygame.K_d] or keys[pygame.K_RIGHT]) * MOVE_SPEED
    player.x -= (keys[pygame.K_a] or keys[pygame.K_LEFT]) * MOVE_SPEED

    # --- Jump / Gravity ---
    if is_jumping:
        if jump_count >= -JUMP_POWER:
            player.y -= (jump_count * abs(jump_count)) * 0.5
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = JUMP_POWER
    else:
        # Apply gravity if not on any platform
        if not any(p.check_collision(player) for p in platforms):
            player.y += GRAVITY

    # --- Snap to Platforms ---
    for p in platforms:
        if p.snap_to_top(player):
            is_jumping = False
            jump_count = JUMP_POWER

    # --- Coin Collection ---
    #TODO
    
    # --- Exit Check ---
    #TODO

    # --- Camera Follow ---
    camera_x = player.centerx - WIDTH // 2
    camera_x = max(0, min(camera_x, LEVEL_WIDTH - WIDTH))

    # --- Boundaries ---
    player.x = max(0, min(player.x, LEVEL_WIDTH - player.width))
    if player.bottom >= HEIGHT:
        game_over = True

    # --- Draw ---
    win.fill(BGCOLOR)

    # Draw platforms
    for p in platforms:
        p.draw(win, camera_x)

    # Draw coins
    #TODO

    # Draw exit
    draw_exit = exit_rect.move(-camera_x, 0)
    pygame.draw.rect(win, EXIT_COLOR, draw_exit)

    # Draw player
    draw_player = player.move(-camera_x, 0)
    pygame.draw.rect(win, PLAYER_COLOR, draw_player)

    # Draw coin counter
    #TODO

    # --- Game Over / Win ---
    if game_over:
        if coins_collected == 10:
            txt1 = font.render("YOU WIN!", True, (0, 150, 0))
        else:
            txt1 = font.render("YOU LOSE!", True, (255, 0, 0))
        txt2 = font.render("Press R to Restart", True, (0, 0, 255))
        win.blit(txt1, txt1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        win.blit(txt2, txt2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        MOVE_SPEED = 0

    pygame.display.update()

pygame.quit()
