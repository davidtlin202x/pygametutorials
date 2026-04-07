import pygame	#imports the pygame module

pygame.init()	#starts the game

#Limit frames to 30 frames per second
clock = pygame.time.Clock()

# Window
HEIGHT = 600
WIDTH = 800
BGCOLOR = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
win = pygame.display.set_mode((WIDTH, HEIGHT))		#sets up a window
pygame.display.set_caption("Simple Game")		#Gives the window a title
x_pos = WIDTH // 2 #sets the x position of the circle to the middle of the window
y_pos = HEIGHT // 2 #sets the y position of the circle to the middle of the window
player = pygame.Rect(x_pos - 20, y_pos - 20, 40, 40) #creates a rectangle to represent the player
game_area = win.get_rect()


# Obstacle
obstacle_width = 20
obstacle_height = 90
obstacle_x = 200
obstacle_y = HEIGHT // 2 - obstacle_height // 2  # center vertically
obstacle = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
OBSTACLE_COLOR = (0, 255, 0)  # green

def get_color():
    r = int(255 * player.centerx / WIDTH)
    b = int(255 * player.centery / HEIGHT)
    return (r, 0, b)

running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            '''
            if event.key == pygame.K_SPACE:
                color = (RED if color == BLUE else BLUE)
            '''

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 5
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += 5

    #Detect a collision based on the BOUNDING RECTANGLE
    if player.colliderect(obstacle):
        OBSTACLE_COLOR = (21,155,21)
    else:
        OBSTACLE_COLOR = (0, 255, 0)

 #prevents the player from moving outside the game area
    win.fill(BGCOLOR)
    player.clamp_ip(game_area) # Check to see if player is outside game area.
    pygame.draw.circle(win, get_color(), player.center, 20)
    pygame.draw.rect(win, OBSTACLE_COLOR, obstacle) 
    pygame.display.update()

pygame.quit()


