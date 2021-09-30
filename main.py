from resource_manager import play_sound_effect
from Modules.Projectiles.Projectile import Projectile
from typing import _SpecialForm
from pygame import key

from pygame.constants import K_h
from Modules.Player.PlayerReport import PlayerReport
from Modules.Enemies.enemy import Enemy
import os
from Modules.settings import GameSettings
from Modules.Player.Player import Player
from sys import exit
import pygame
from random import choice, randint


pygame.init()               # initialize pygame

settings = GameSettings()   # import common game settings


# create screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Kjetil the Game")

# manage game fonts
font_path = os.path.join("Resources", "Fonts", "Pixeltype.ttf")
game_font = pygame.font.Font(font_path, 24)
game_font_2 = pygame.font.Font(font_path, 48)
game_font_3 = pygame.font.Font(font_path, 72)


# background music players
menu_music_path = os.path.join("resources","music","menu_music.ogg")
menu_music = pygame.mixer.Sound(menu_music_path)
menu_music.set_volume(0.6)
menu_music.play(loops=-1)

battle_music_path = os.path.join("resources","music","game_music.ogg")
battle_music = pygame.mixer.Sound(battle_music_path)
battle_music.set_volume(0.6)

# get kjetil image
kjetil_image_path = os.path.join("resources","images","kjetil.png")
kjetil_image = pygame.image.load(kjetil_image_path)





clock   = pygame.time.Clock()   # Game clock for controlling framerate
FPS     = 60                    # Value for game framerate

player_report       = PlayerReport(0, [], 0, 0, 0, False, None, False)   # player report for sprites


sprites_on_screen   = 0     # sprites on screen for spawn
sprites_killed      = 0     # sprites killed for score
boss_spawn_countdown = randint(10,15)   # countdown for boss spawn

player_health   = 200   # player health for health bar
shit            = 0     # player shit bonus for shit shoot
sperm           = 0     # player sperm for sperm shot

player_dead     = False     # True when player dies 
player_dead_timer = 6       # Timer for player death
music_fadeout   = False      # trigger music fadeout


game_active = False
fresh_start = True
show_help   = False




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

    health_text = game_font.render("Health", True, "white")

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

    shit_txt = f'{availible} / 1 Brown Torpedo'
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

    sperm_txt = f'{availible} / 1 Cumshot'
    sperm_text = game_font.render(sperm_txt, True, "white")

    screen.blit(spermbar_surface, pos)
    screen.blit(sperm, pos)
    screen.blit(sperm_text, (220, 74))

# draw kill score
def draw_kill_score():

    kill_text = f"{sprites_killed} bro's and hoe's smacked down"
    box = game_font_2.render(kill_text, True, "pink")
    
    screen.blit(box, (500, 40))


# draw break screen
def draw_break_screen():

    title_text = game_font_3.render("Kjetil, The Game", False, "brown")
    title_rect = title_text.get_rect(center=(600, 60))

    kjetil_rect = kjetil_image.get_rect(center=(600, 220))

    text = [
        "Welcome",
        "",
        "GAME OVER",
        f"You gave {sprites_killed} bitches and assholes a lesson",
        "Press Spacebar to start a new game",
        'Press "H" to see instructions'
    ]

    line_1 = game_font_2.render(text[0], False, "brown")
    line_2 = game_font_2.render(text[1], False, "brown")
    line_3 = game_font_2.render(text[2], False, "brown")
    line_4 = game_font_2.render(text[3], False, "brown")
    line_5 = game_font_2.render(text[4], False, "brown")
    line_6 = game_font_2.render(text[5], False, "brown")

    line_1_rect = line_1.get_rect(center=(600,400))
    line_2_rect = line_2.get_rect(center=(600,450))
    line_3_rect = line_3.get_rect(center=(600,400))
    line_4_rect = line_4.get_rect(center=(600,450))
    line_5_rect = line_5.get_rect(center=(600,500))
    line_6_rect = line_6.get_rect(center=(600,550))


    screen.fill((254,255,255))
    screen.blit(title_text, title_rect)
    screen.blit(kjetil_image, kjetil_rect)

    if fresh_start:
        screen.blit(line_1, line_1_rect)
        screen.blit(line_2, line_2_rect)
    else:
        screen.blit(line_3, line_3_rect)
        screen.blit(line_4, line_4_rect )
    
    screen.blit(line_5, line_5_rect)
    screen.blit(line_6, line_6_rect)
    
# draw help screen    
def draw_help_screen():
    
    text = [
        'Press "A" and "D" to move left and right.',
        'Press "SPACEBAR" to jump.',
        'Press "S" for a classic bitchslap to the face.',
        'Press "Q" for CumShot attack if your cock is loaded.', 
        'Press "E" for Assblast attack if your ass is loaded.',
        '',
        "You will be fighting hunkes and bitches, and sometimes a fancypants.",
        'Defeating a hunk will load up your ass with diarrhea.',
        "Defeating a bitch will load ip your cock with cum.",
        "Spraying a fancypants with diarrhea or cum will give you health.",
        "",
        'Be aware of your cumload and your shitload.', 
        'If load more than 1, you will explode!!!',
        "",
        "Oh, by the way:",
        "Chuck Norris or Arnold Schwarznegger might show up to kick your ass...",
        "",
        "Be like Kjetil, Be awesome!!!"
    ]

    lines = []

    rects = []

    for t in text:
        line = game_font_2.render(t, False, "brown")
        lines.append(line)
    
    y = 30

    for line in lines:
        rect = line.get_rect(midleft = (20, y))
        rects.append(rect)
        y += 30
    
    l = len(text)

    screen.fill((254,255,255))

    for i in range(l):
        screen.blit(lines[i], rects[i])



####    SPRITES    ###

player = pygame.sprite.GroupSingle()    # player sprite group
enemies = pygame.sprite.Group()         # enemies sprite group
projectiles = pygame.sprite.Group()     # projectiles sprite group


# start new game
def start_game():
    global player, enemies, sprites_killed, player_dead, player_dead_timer

    player_dead = False
    player_dead_timer = 6

    player.add(Player())
    enemies.empty()
    sprites_killed = 0
    menu_music.stop()
    play_sound_effect("start")
    battle_music.play(loops = -1)

# add spawn event
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 2000)

# main game loop
while True:

    # game events here
    for event in pygame.event.get():

        # check if quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:

            if show_help and event.type == pygame.KEYDOWN:
                show_help = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                show_help = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                fresh_start = False
                game_active = True
                start_game()
        
        if game_active:

            
            if event.type == spawn_timer:

                if sprites_on_screen <= 0:
                    e = choice([0,1])
                    enemies.add(Enemy(e))

                if (sprites_on_screen < 3):
                    e = choice([0,1,0,1,0,1,2])
                    enemies.add(Enemy(e))

                if (boss_spawn_countdown <= 0):
                    e = choice([3,4])
                    enemies.add(Enemy(e))
                    boss_spawn_countdown = randint(11,16)
                   

    if game_active:
        
        # draw background and gui elements
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

            if report.killed: 
                sprites_killed += 1   # update sprites killed
                sprites_on_screen -= 1
                boss_spawn_countdown -= 1

            enemies_report.append(report)           # gather enemy report





        ### HANDLE PLAYER SPRITE ###

        player.draw(screen)         # draw player sprite

        player_report = player.sprites()[0].update(enemies_report)    # update player with enemies report
        
        player_health   = player_report.health      # get player health
        shit            = player_report.shit        # get player shit
        sperm           = player_report.sperm       # get player sperm

        player_dead = player_report.player_dead     # report dead player

        # add projectile if shot
        if player_report.shoot != None:
            p = Projectile(player_report.shoot, player_report.pos, player_report.direction)
            projectiles.add(p)

        # draw and update projectiles
        projectiles.draw(screen)
        projectiles.update()

        # check projectile vs enemy collison
        res = pygame.sprite.groupcollide(projectiles, enemies, False, False)
        if res != {}:
            
            # get sprites hit by load
            sprites = list(res.values())[0]
            bullet = list(res.keys())[0]

            # itterate sprites
            for enemy in sprites:

                # add health if fancypants
                if enemy.sprite_index == 2:
                    player.sprites()[0].player_health += 50
                    if player.sprites()[0].player_health > 200:
                        player.sprites()[0].player_health = 200
                    enemy.sprite_is_dead = True
                    bullet.kill()

                enemy.sprite_health -= 50

                if not enemy.sprite_is_dead:
                    bullet.kill()

        if player_dead:

            if music_fadeout == False:
                battle_music.fadeout(1000)
                music_fadeout = True

            player_dead_timer -= 0.1

        if player_dead_timer < 0:
            menu_music.play(loops = -1)
            play_sound_effect("game_over")
            game_active = False
            music_fadeout = False

    else:
        if show_help:
            draw_help_screen()
        else:
            draw_break_screen()



    # update display
    pygame.display.update()
    # game tick
    clock.tick(FPS)