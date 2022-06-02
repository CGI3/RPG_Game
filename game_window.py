import pygame

pygame.init()

#Sets a fixed frame rate so that animations don't play at different speeds
#Set frame rate
time = pygame.time.Clock()
#Sets to 60 frames per second
fps = 60

# Game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Life RPG')

#Loading Images into display

#Background Image
#Do this outside game loop, otherwise it will happen in each iteration
#This code doesn't load it into display, it just loads it into memory
background_image = pygame.image.load('images/Background/forest_background_by_sendrawz_da57kln-fullview.jpg').convert_alpha()
#Panel Image
panel_image = pygame.image.load('images/Icons/panel.png').convert_alpha()


#Display the picture: function for drawing background
def draw_background():
    #blit is the function for putting things on the screen
    # (x, y) coordinates. 0, 0 places at top left corner
    screen.blit(background_image, (0, -170))

#Function for drawing the panel below the background display
def draw_panel():
    screen.blit(panel_image, (0, screen_height - bottom_panel))


# Loop to run the game display
run = True
while run:

    #Sets while loop to run at a fixed 60 fps
    time.tick(fps)

    #Draw background by calling draw_background function
    draw_background()

    #Draw panel function
    draw_panel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #This code is going to be running a bunch of functions in the while loop. This .update() command
    #is used so that your display updates with that functions code
    pygame.display.update()

pygame.quit()
