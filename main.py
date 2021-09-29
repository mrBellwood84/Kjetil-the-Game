from Modules.Player.PlayerReport import PlayerReport
from Modules.Enemies.enemy import Enemy
import os
from Modules.settings import GameSettings
from Modules.Player.Player import Player
from sys import exit
import pygame


pygame.init()               # initialize pygame

settings = GameSettings()   # import common game settings


# create screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Kjetil the Game")


clock   = pygame.time.Clock()   # Game clock for controlling framerate
FPS     = 60                    # Value for game framerate

player_report       = PlayerReport(0)   # player report for sprites


sprites_on_screen   = 0     # sprites on screen
sprites_killed      = 0     # sprites killed

# Function for drawing background
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



    ### HANDLE ENEMY SPRITES ###

    enemies_report = []             # hold enemy reports
    enemies.draw(screen)            # draw enemy sprites on screen
    sprites = enemies.sprites()     # get sprites array

    sprites_on_screen = len(sprites)    # update sprite on screen value

    for sprite in sprites:               # update and collect report for each sprite

        report = sprite.update(player_report)   # update sprite with player report
        
        if report.killed: sprites_killed += 1   # update sprites killed

        enemies_report.append(report)           # gather enemy report



    ### HANDLE PLAYER SPRITE ###

    player.draw(screen)         # draw player sprite

    player_report = player.sprites()[0].update(enemies_report)    # update player with enemies report




    # update display
    pygame.display.update()
    # game tick
    clock.tick(FPS)