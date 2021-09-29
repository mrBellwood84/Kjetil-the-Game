from typing import _SpecialForm
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

game_font = pygame.font.SysFont(None, 24)
game_font_2 = pygame.font.SysFont(None, 48)


clock   = pygame.time.Clock()   # Game clock for controlling framerate
FPS     = 60                    # Value for game framerate

player_report       = PlayerReport(0, [], 0, 0, 0, False)   # player report for sprites


sprites_on_screen   = 0     # sprites on screen for spawn
sprites_killed      = 0     # sprites killed for score

player_health   = 200   # player health for health bar
shit            = 0     # player shit bonus for shit shoot
sperm           = 0     # player sperm for sperm shot



# Function for drawing background
def draw_game_background():
    bg_image_path = os.path.join("resources", "images","oslo.png")
    bg_image = pygame.image.load(bg_image_path).convert()
    bg_image = pygame.transform.scale(bg_image, (settings.screen_width, settings.screen_height))
    screen.blit(bg_image, (0,0))

# draw health bar
def draw_health_bar():

    global player_health

    size = (200, 20)            # static size for health bar
    pos = (10,10)               # static position for health bar

    healthbar_surface = pygame.Surface(size)    # healthbar surface
    healthbar_surface.fill("red")               # healthbar fill

    if player_health < 0: player_health = 0

    health = pygame.Surface((int(player_health), size[1]))
    health.fill("green")

    health_text = game_font.render("HELSE", True, "white")

    screen.blit(healthbar_surface, pos)
    screen.blit(health, pos)
    screen.blit(health_text, (220, 14))

# draw shit bar
def draw_shit_bar():

    global shit

    availible = 0
    while shit > 1:
        availible += 1
        shit -= 1
    
    progress = int(shit * 200)

    size = (200, 20)
    pos = (10, 40)

    shitbar_surface = pygame.Surface(size)
    shitbar_surface.fill("gray")

    shit = pygame.Surface((progress, 20))
    shit.fill("brown")

    shit_txt = f'{availible} / 3 SPRUTBÆSJ'
    shit_text = game_font.render(shit_txt, True, "white")

    screen.blit(shitbar_surface, pos)
    screen.blit(shit, pos)
    screen.blit(shit_text, (220, 44))

# draw sperm bar
def draw_sperm_bar():
    global sperm

    availible = 0
    while sperm > 1:
        availible += 1
        sperm -= 1
    
    progress = int(sperm * 200)

    size = (200, 20)
    pos = (10, 70)

    spermbar_surface = pygame.Surface(size)
    spermbar_surface.fill("gray")

    sperm = pygame.Surface((progress, 20))
    sperm.fill("white")

    sperm_txt = f'{availible} / 3 SPØNKSHOTS'
    sperm_text = game_font.render(sperm_txt, True, "white")

    screen.blit(spermbar_surface, pos)
    screen.blit(sperm, pos)
    screen.blit(sperm_text, (220, 74))


# draw kill score
def draw_kill_score():

    kill_text = f'{sprites_killed} FIENDER SLAKTA NED'
    box = game_font_2.render(kill_text, True, "pink")
    
    screen.blit(box, (500, 40))




####    SPRITES    ###

# add player sprite
player = pygame.sprite.GroupSingle()
player.add(Player())

# add enemy sprite group
enemies = pygame.sprite.Group()
foe = Enemy(1)
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
    draw_health_bar()
    draw_shit_bar()
    draw_sperm_bar()
    draw_kill_score()



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
    
    player_health   = player_report.health      # get player health
    shit            = player_report.shit        # get player shit
    sperm           = player_report.sperm       # get player sperm




    # update display
    pygame.display.update()
    # game tick
    clock.tick(FPS)