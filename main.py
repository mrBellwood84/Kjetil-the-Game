from import_resource import get_JanTheMan
from Modules.Player.Player import Player
from sys import exit
import pygame


# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Kjetil the Game")

# set clock
clock = pygame.time.Clock()


####    BACKGROUND    ####
sky_surf = pygame.Surface((1200,450))
sky_surf.fill("blue")

ground_surf = pygame.Surface((1200,150))
ground_surf.fill("green")


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
            quit()
        
        # other events here
    
    # draw background:
    screen.blit(sky_surf, (0,0))
    screen.blit(ground_surf, (0,450))


    player.draw(screen)
    player.update()

    # update display
    pygame.display.update()
    # game tick
    clock.tick(60)