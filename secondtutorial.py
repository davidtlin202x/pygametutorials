import pygame	#imports the pygame module

pygame.init()	#starts the game

# CONSTANTS
HEIGHT = 600
WIDTH = 800
BGCOLOR = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))		#sets up a window
pygame.display.set_caption("Simple Game")		#Gives the window a title
x_pos = WIDTH // 2 #sets the x position of the circle to the middle of the window
y_pos = HEIGHT // 2 #sets the y position of the circle to the middle of the window

color = (128, 0, 128)

def get_color():
    r = int(255 * x_pos / WIDTH)
    b = int(255 * y_pos / HEIGHT)
    return (r, 0, b)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                color = (RED if color == BLUE else BLUE)
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x_pos -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x_pos += 5
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y_pos -= 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y_pos += 5
        
    win.fill(BGCOLOR)
    pygame.draw.circle(win, get_color(), (x_pos, y_pos), 40)
    pygame.display.update()

pygame.quit()
