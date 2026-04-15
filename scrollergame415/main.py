import pygame
from platforms import Platform
from enemy import Enemy

pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
LEVEL_WIDTH = 2000

PLAYER_SIZE = 40
MOVE_SPEED = 5
GRAVITY = 5
JUMP_POWER = 10

COIN_SIZE = 20
WIN_COINS = 3

PLAYER_COLOR = (0, 0, 255)
BGCOLOR = (255, 255, 255)
COIN_COLOR = (255, 215, 0)
EXIT_COLOR = (0, 0, 0)

# --- Setup ---
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Jump Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# --- Player ---
# to do : Load the sprites, and scale them
player_sprite = pygame.image.load(
    "platformer_with_coins/images/C_SPRITE.png"
).convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (PLAYER_SIZE, PLAYER_SIZE))
facing_right = True
player = pygame.Rect(50, HEIGHT - 100, PLAYER_SIZE, PLAYER_SIZE)

# --- Game State ---
state = "playing"  # "playing", "game_over"
is_jumping = False
jump_count = JUMP_POWER
camera_x = 0


# --- Level Data ---
platforms = [
    Platform(0, HEIGHT - 50, WIDTH // 3, 20),
    Platform(WIDTH // 3, HEIGHT - 200, WIDTH // 3, 20),
    Platform(2 * WIDTH // 3, HEIGHT - 350, WIDTH // 3, 20),
    Platform(WIDTH, HEIGHT - 259, WIDTH // 3, 20),
    Platform(WIDTH + WIDTH // 3, HEIGHT - 120, WIDTH // 3, 20),
    Platform(WIDTH + 2 * WIDTH // 3, HEIGHT - 300, WIDTH // 2, 20),
    Platform(WIDTH + 5 * WIDTH // 4, HEIGHT - 400, WIDTH // 3, 20),
    Platform(WIDTH + 7 * WIDTH // 3, HEIGHT - 200, WIDTH // 3, 20)
]

def reset_coins():
    return [
        pygame.Rect(150, HEIGHT - 100, COIN_SIZE, COIN_SIZE),
        pygame.Rect(350, HEIGHT - 250, COIN_SIZE, COIN_SIZE),
        pygame.Rect(550, HEIGHT - 400, COIN_SIZE, COIN_SIZE),
    ]

coins = reset_coins()
coins_collected = 0

enemies = [
    Enemy(platforms[1], 50),
    Enemy(platforms[3], 100),
    Enemy(platforms[5], 30),
]

exit_rect = pygame.Rect(LEVEL_WIDTH - 60, 120, 40, 70)


# --- Reset Game ---
def reset_game():
    global player, is_jumping, jump_count, coins, coins_collected, state

    player.topleft = (50, HEIGHT - 100)
    is_jumping = False
    jump_count = JUMP_POWER
    coins = reset_coins()
    coins_collected = 0
    state = "playing"


# --- Game Loop ---
running = True

while running:
    clock.tick(30)

    # --- Events ---
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_q):
            running = False

        if state == "game_over":
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                reset_game()

        if state == "playing" and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            on_platform = any(
                p.rect.top - 10 <= player.bottom <= p.rect.top + 10
                and player.right > p.rect.left
                and player.left < p.rect.right
                for p in platforms
            )
            if on_platform:
                is_jumping = True
                jump_count = JUMP_POWER

    # =========================
    # GAME LOGIC (ONLY PLAYING)
    # =========================
    if state == "playing":

        # --- Movement ---
        keys = pygame.key.get_pressed()
        player.x += (keys[pygame.K_d] or keys[pygame.K_RIGHT]) * MOVE_SPEED
        player.x -= (keys[pygame.K_a] or keys[pygame.K_LEFT]) * MOVE_SPEED

        # --- Jump / Gravity ---
        if is_jumping:
            if jump_count >= -JUMP_POWER:
                player.y -= int(jump_count * abs(jump_count) * 0.5)
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = JUMP_POWER
        else:
            if not any(p.check_collision(player) for p in platforms):
                player.y += GRAVITY

        # --- Platform snapping ---
        for p in platforms:
            if p.snap_to_top(player):
                is_jumping = False
                jump_count = JUMP_POWER

        # --- Coins ---
        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                coins_collected += 1

        # --- Exit ---
        if player.colliderect(exit_rect):
            if coins_collected == WIN_COINS:
                state = "game_over"
            else:
                player.right = exit_rect.left

        # --- Camera ---
        camera_x = max(0, min(player.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))

        # --- Boundaries ---
        player.x = max(0, min(player.x, LEVEL_WIDTH - player.width))

        if player.bottom >= HEIGHT:
            state = "game_over"

        # --- Enemies ---
        for enemy in enemies:
            enemy.movement()
            if enemy.rect.colliderect(player):
                state = "game_over"

    # =========================
    # DRAWING (ALWAYS)
    # =========================
    win.fill(BGCOLOR)

    for p in platforms:
        p.draw(win, camera_x)

    for coin in coins:
        pygame.draw.ellipse(win, COIN_COLOR, coin.move(-camera_x, 0))

    pygame.draw.rect(win, EXIT_COLOR, exit_rect.move(-camera_x, 0))

    draw_pos = player.move(-camera_x, 0)

    draw_player = player.move(-camera_x, 0)
    pygame.draw.rect(win, PLAYER_COLOR, draw_player)

    win.blit(
        font.render(f"Coins: {coins_collected}/{WIN_COINS}", True, (0, 0, 0)),
        (20, 20),
    )

    for enemy in enemies:
        enemy.draw(win, camera_x)

    # --- Game Over Screen ---
    if state == "game_over":
        text = "YOU WIN!" if coins_collected == WIN_COINS else "YOU LOSE!"
        color = (0, 150, 0) if coins_collected == WIN_COINS else (255, 0, 0)

        win.blit(font.render(text, True, color),
                 (WIDTH // 2 - 80, HEIGHT // 2 - 50))

        win.blit(font.render("Press R to Restart", True, (0, 0, 255)),
                 (WIDTH // 2 - 150, HEIGHT // 2 + 20))

    pygame.display.update()

pygame.quit()
