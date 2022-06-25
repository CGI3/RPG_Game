import pygame
import random

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

#Define the game variables
current_fighter = 1
#Knight and 2 thieves
total_fighters = 3
#Don't want it to cycle through them all and go too quickly. Want there to be
#time between the actions
action_cooldown = 0
action_wait_time = 90

# Define fonts
text_font = pygame.font.SysFont('Times New Roman', 26)

# Define font colors
red = (225, 0, 0)
green = (0, 255, 0)


#Loading Images into display

#Background Image
#Do this outside game loop, otherwise it will happen in each iteration
#This code doesn't load it into display, it just loads it into memory
background_image = pygame.image.load('images/Background/thick_forest.jpg').convert_alpha()
#Panel Image
panel_image = pygame.image.load('images/Icons/panel.png').convert_alpha()

#create function for drawing text
def draw_text(text, font, text_color, x, y):
    image = font.render(text, True, text_color)
    screen.blit(image, (x, y))

#Display the picture: function for drawing background
def draw_background():
    #blit is the function for putting things on the screen
    # (x, y) coordinates. 0, 0 places at top left corner
    screen.blit(background_image, (0, -170))

#Function for drawing the panel below the background display
def draw_panel():
    # Draw the rectangle panel beneath display
    screen.blit(panel_image, (0, screen_height - bottom_panel))
    # Show the knights stats
    draw_text(f'{knight.name} HP: {knight.hp}', text_font, red, 100, screen_height - bottom_panel + 10)

    # Iterates through thief list to give stats
    for count, i in enumerate(thief_list):
        draw_text(f'{i.name} HP: {i.hp}', text_font, red, 550, (screen_height - bottom_panel + 10) + count * 60)


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
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        #Deal damage to the opposing enemy
        random_number = random.randint(-5, 5)
        damage = self.strength + random_number
        target.hp -= damage
        #Set variables so that when attacking, the attack animation happens
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #Update with new health
        self.hp = hp

        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


#Characters
knight = Knight(200, 260, 'Knight', 30, 10, 3)
thief1 = Knight(580, 270, 'Thief', 20, 6, 1)
thief2 = Knight(700, 270, 'Thief', 20, 6, 1)

thief_list = []
thief_list.append(thief1)
thief_list.append(thief2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
thief1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, thief1.hp, thief1.max_hp)
thief2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, thief2.hp, thief2.max_hp)


# Loop to run the game display
run = True
while run:

    #Sets while loop to run at a fixed 60 fps
    time.tick(fps)

    #Draw background by calling draw_background function
    draw_background()

    #Draw panel function
    draw_panel()
    knight_health_bar.draw(knight.hp)
    thief1_health_bar.draw(thief1.hp)
    thief2_health_bar.draw(thief2.hp)

    #Update (draw) characters
    knight.update()
    knight.draw()

    for thief in thief_list:
        thief.update()
        thief.draw()

    #Player action
    if knight.alive:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                #Look for player action
                #Attack
                knight.attack(thief1)
                current_fighter += 1
                action_cooldown

    #Enemy action
    for count, thief in enumerate(thief_list):
        if current_fighter == 2 + count:
            if thief.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #Attack
                    thief.attack(knight)
                    current_fighter += 1
                    action_cooldown = 0
            else:
                current_fighter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #This code is going to be running a bunch of functions in the while loop. This .update() command
    #is used so that your display updates with that functions code
    pygame.display.update()

pygame.quit()
