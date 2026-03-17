import pygame	#imports the pygame module

pygame.init()	#starts the game

# Window
HEIGHT = 600
WIDTH = 800
BGCOLOR = (255, 255, 255)
BLUE = (0, 0, 255)
win = pygame.display.set_mode((WIDTH, HEIGHT))		#sets up a window
pygame.display.set_caption("Simple Game")		#Gives the window a title
x_pos = WIDTH // 2 #sets the x position of the circle to the middle of the window
y_pos = HEIGHT // 2 #sets the y position of the circle to the middle of the window

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x_pos -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x_pos += 5
        
    color = BLUE
    win.fill(BGCOLOR)
    pygame.draw.circle(win, color, (x_pos, y_pos), 40)
    pygame.display.update()

pygame.quit()
