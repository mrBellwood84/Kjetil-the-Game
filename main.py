from Modules.settings import GameSettings
from Modules.Player.Player import Player
from sys import exit
import pygame


# initialize pygame
pygame.init()

## SETTINGS

# get common settings for settings class
settings = GameSettings()

# create screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Kjetil the Game")

# Clock and framerate
clock = pygame.time.Clock()
FPS = 60


####    BACKGROUND    ####
# DEV :: fix this
bg_image = pygame.image.load("oslo.png").convert()
bg_image = pygame.transform.scale(bg_image, (settings.screen_width, settings.screen_height))


####    Player    ###
player = pygame.sprite.GroupSingle()
player.add(Player())


# main game loop
while True:

    # game events here
    for event in pygame.event.get():

        # check if quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # other events here
    
    # draw background:
    screen.blit(bg_image, (0,0))


    player.draw(screen)
    player.update()

    # update display
    pygame.display.update()
    # game tick
    clock.tick(FPS)