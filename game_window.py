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
background_image = pygame.image.load('images/Background/thick_forest.jpg').convert_alpha()
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


#Creating a player and enemies is easier using Classes
#fighter class
class Knight():
    #constructor
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0:idle 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        #Load Idle Images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'images/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Load  Attack Images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'images/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        animation_cooldown = 100
        #handles animation
        #update image to latest, so its appropriate for animation
        self.image = self.animation_list[self.action][self.frame_index]
         #Check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #If the animation runs out, reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def draw(self):
        screen.blit(self.image, self.rect)

#Characters
knight = Knight(200, 260, 'Knight', 30, 10, 3)
thief1 = Knight(580, 270, 'Thieves', 20, 6, 1)
thief2 = Knight(700, 270, 'Thieves', 20, 6, 1)

thief_list = []
thief_list.append(thief1)
thief_list.append(thief2)


# Loop to run the game display
run = True
while run:

    #Sets while loop to run at a fixed 60 fps
    time.tick(fps)

    #Draw background by calling draw_background function
    draw_background()

    #Draw panel function
    draw_panel()

    #Update (draw) characters
    knight.update()
    knight.draw()

    for thief in thief_list:
        thief.update()
        thief.draw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #This code is going to be running a bunch of functions in the while loop. This .update() command
    #is used so that your display updates with that functions code
    pygame.display.update()

pygame.quit()
