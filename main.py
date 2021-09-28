from Modules.Enemies.enemy import Enemy
import os
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
clock = pygame.time.Clock()     # game clock
FPS = 60                        # static framerate

# game variables
player_pos = 0                  # hold player position for enemy movement [rect left, rect right]

# DEV :: player health
p_health = 100



# Game loop functions
def draw_game_background():
    bg_image_path = os.path.join("resources", "images","oslo.png")
    bg_image = pygame.image.load(bg_image_path).convert()
    bg_image = pygame.transform.scale(bg_image, (settings.screen_width, settings.screen_height))
    screen.blit(bg_image, (0,0))


####    SPRITES    ###
# add player sprite
player = pygame.sprite.GroupSingle()
player.add(Player())

# add enemy sprite group
enemies = pygame.sprite.Group()
foe = Enemy(4)
enemies.add(foe)

# main game loop
while True:

    # game events here
    for event in pygame.event.get():

        # check if quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    
    # draw background:
    draw_game_background()


    # draw enemies
    enemies.draw(screen)
    
    # update enemies individualy for attack results
    sprites = enemies.sprites()
    for s in sprites:
        res = s.update(player_pos)
        if res != None:
            p_health -= res
            print(p_health)


    # draw and update player
    player.draw(screen)
    player.update()
    player_pos = player.sprites()[0].player_x_center()





    # update display
    pygame.display.update()
    # game tick
    clock.tick(FPS)