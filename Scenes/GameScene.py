
from random import randint, choice
import pygame
from pygame.constants import QUIT
import sys, math

from config import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from Core.App import App
import Core.utility as util
from Sprites.Player import Player, PlayerData
from Sprites.Enemy import Enemy
from paths import image_dir, battle_music_path
from Scenes.assets import gamefont_status_bar, gamefont_score_text

class GameScene:
    """ class for gamescene """

    # constuctor
    def __init__(self):

        # sprite groups
        self.player         = pygame.sprite.GroupSingle()   # player sprite group
        self.enemies        = pygame.sprite.Group()         # enemies sprite group
        self.projectiles    = pygame.sprite.Group()         # projectile sprite group


        # gui elements
        self.health_bar     = 0
        self.shit_lvl       = 0
        self.cum_lvl        = 0


        # background music
        self.music = pygame.mixer.Sound(battle_music_path)
        self.music.set_volume(0.4)
        self.music.play(loops = -1)


        # class variables
        self.sprites_on_screen  = 0
        self.boss_count_down    = randint(8,12)

        # spawn control for fancy pants
        self.fancypants             = 0         # hold amounts of fancypants on screen
        self.non_fancypants_spawn   = 0         # amount of spawns between fancypants

        self.player_data    = PlayerData()  # hold player data

        self.end_count_down     = 6         # Countdown for play end
        self.fading_music       = False     # True when fadeout initated
        self.gameover_played    = False     # set true when gameover tune is played

        # add user event
        self.spawn_timer = pygame.USEREVENT + 1          # create spawn timer event
        pygame.time.set_timer(self.spawn_timer, 2000)    # set timer to event


        # boolean for running scene
        self.run_scene = True

        # add player
        self.player.add(Player())


    # draw method for scene
    def run(self):
        """ contain a gameloop sequence for the scene  """

        while self.run_scene:
        # reset values and prep screen
            enemy_data = []             # create list for enemy data

            self.handle_game_events()   # handle game events

            self.fancypants = 0         # reset value for fancypants on screen value

            self.create_background()    # create background
            self.draw_game_score()      # draw game score
            self.draw_game_stats()      # draw game stats


            # -- HANDLE ENEMY SPRITES -- ##
            self.enemies.draw(App.SCREEN)   # draw sprites on screen

            for sprite in self.enemies.sprites():       # itterate each sprite to gather reports
                data = sprite.update(self.player_data)  # gather data
                enemy_data.append(data)                 # apped data to list

                if sprite.sprite_index == 2:            # check amounts of fancypants spawned
                    self.fancypants += 1                # for spawn controll

            self.handle_enemy_data(enemy_data)          # handle enemy data 
            
            ## -- HANDLE PLAYER -- ##
            self.player.draw(App.SCREEN)                # draw player on sceen

            # update sprite and collect data
            self.player_data = self.player.sprites()[0].update(enemy_data)  

            # handle updatet player data
            self.handle_player_data()                   # Handle data from player
            

            # -- HANDLE PROJECTILES -- ##
            self.projectiles.draw(App.SCREEN)           # draw projectiles
            self.projectiles.update()                   # update projectiles
            self.handle_projectile_collision()          # handle projectile collisions

            # update screen and tick
            pygame.display.update()
            App.CLOCK.tick(App.FPS)


    # create background
    def create_background(self):
        """Create scene background"""

        # get image file
        image = util.get_surface(image_dir, "oslo")

        # resize image to fit sceen
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # draw background to sceen
        App.SCREEN.blit(image, (0,0))


    # create status bar
    def create_status_bar(self, status_color, status_value, status_txt, y_pos):

        # set position for status bar
        pos = (20, y_pos + 20)

        # create background fill for status bar
        status_bar_background = pygame.Surface((200, 20))
        status_bar_background.fill((50,50,50))

        # create the bar that represent the status value
        status_bar_foreground = pygame.Surface((status_value, 20))
        status_bar_foreground.fill(status_color)

        # create the status text
        status_text = gamefont_status_bar.render(status_txt, False, (200,200,200))

        # print status bar to screen
        App.SCREEN.blit(status_bar_background, pos)
        App.SCREEN.blit(status_bar_foreground, pos)
        App.SCREEN.blit(status_text, (230, pos[1] + 2))


    # create health bar
    def draw_game_stats(self):

        hp = self.player_data.health        # get health ponts
        if hp < 0: hp = 0                   # ensure hp not below 0

        # get shit values for status bar
        shit_stat       = self.player_data.shit_bonus
        shit_avalible   = math.floor(shit_stat)
        shit_bar_value  = (shit_stat - shit_avalible) * 200
        shit_text       = f'{shit_avalible} / 1 Brown Torpedo'
        
        # get cum values for status bar
        cum_stat        = self.player_data.cum_bonus
        cum_availble    = math.floor(cum_stat)
        cum_bar_value   = (cum_stat - cum_availble) * 200
        cum_text        = f'{cum_availble} / 1 Cumshots'

        # draw status bars
        self.create_status_bar("green", hp, "Health", 0)
        self.create_status_bar("#9f8303", shit_bar_value, shit_text, 30)
        self.create_status_bar("#fbf5f9", cum_bar_value, cum_text, 60 )


    # draw game score to screen
    def draw_game_score(self):
        
        text = f"{App.Store.sprites_killed} bro's and hoe's smacked down"
        box  = gamefont_score_text.render(text, True, 'pink')

        App.SCREEN.blit(box, (500, 40))


    # handle game events
    def handle_game_events(self):
        " handle game events for scene sequence "

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            
            if self.player_data.is_dead:
                return

            if event.type == self.spawn_timer:

                self.spawn_control()


    # handle enemy data
    def handle_enemy_data(self, enemy_data_list):

        self.sprites_on_screen = len(enemy_data_list)   # get numbers of sprites on screen
        
        # itterate data objects from sprites
        for data in enemy_data_list:

            if data.sprite_killed:              # if sprite was killed
                self.boss_count_down -= 1       # decrement boss spawn counter
                self.sprites_on_screen -= 1     # decrement sprites on sceen value
                App.Store.sprites_killed += 1   # add kill score


    # handle player projectile and death from player data
    def handle_player_data(self):

        if self.player_data.is_dead:        # if player is dead

            if not self.fading_music:
                self.fading_music = True
                self.music.fadeout(2000)

            self.end_count_down -= 0.1      # start decrementing end countdown

            if self.end_count_down < 0:                 # when countdown reach 0
                if not self.gameover_played:            # if game over not played
                    self.gameover_played = True         # set played as true
                    util.play_sound_effect("game_over",1)   # play game over sound effect

                self.end_game()

            return      # and end here if player is dead

        # if player data contain projectile
        if self.player_data.projectile != None:
            # add projectile to
            self.projectiles.add(self.player_data.projectile) 


    # handle projectile collisions
    def handle_projectile_collision(self):
        
        # get collisions
        collisions = pygame.sprite.groupcollide(self.projectiles, self.enemies, False, False)

        if collisions == {}: return     # return if no collisions

        bullet = list(collisions.keys())[0]         # get projectile sprite
        sprites = list(collisions.values())[0]      # get enemy sprites

        # itterate enemy sprites
        for enemy in sprites:
            
            # if enemy sprite is fancypants
            if enemy.sprite_index == 2:                         
                self.player.sprites()[0].player_health += 50        # increment health
                if self.player.sprites()[0].player_health > 200:    # check not above hp limit
                    self.player.sprites()[0].player_health = 200    # ensure hp limit

            enemy.sprite_health -= 50       # remove 50 hp from sprite
            enemy.damage_active = True

            if not enemy.sprite_is_dead:    # if sprite is not dead
                bullet.kill()


    # controll enemey spawning
    def spawn_control(self):

        # arrays for random choice for spawning
        regular         = [0,0,1,1,2]   # hold regular spawn choice
        fancypants_high = [0,1,2]       # hold higher chance for fancypants
        no_fancypants   = [0,1]         # prite only
        boss_spawn      = [3,4]         # boss spawn only

        # return if high number of sprites
        if self.sprites_on_screen > 3:
            print("no spawn")
            return

        # spawn boss if boss spawn counted down
        if self.boss_count_down < 0:
            self.enemies.add(Enemy(choice(boss_spawn)))     # spawn random boss
            self.boss_count_down = randint(8,12)            # set new boss count down
            return
        
        # dont spawn fancypants of exist on screen
        if self.fancypants >= 1:
            self.enemies.add(Enemy(choice(no_fancypants)))  # spawn random enemy sprite
            self.non_fancypants_spawn += 1                  # increment non fancypants spawn
            return
        

        # higher fancypants chance if low health or long time since last one
        if self.player_data.health < 25 or self.non_fancypants_spawn > 8:
            e = choice(fancypants_high)
        # normal spawn
        else:
            e = choice(regular) 


        if e == 2:                              # if random sprite is fancypants
            self.non_fancypants_spawn = 0       # reset non fancy pants counter
        else:                                   # else
            self.non_fancypants_spawn += 1      # increment non fancypants counter

        self.enemies.add(Enemy(e))              # spawn fancypants
    




    # quit game scene loop and returning to menu screen
    def end_game(self):

        App.set_active_scene(App, "menu_scene")
        self.run_scene = False
    

if __name__ == "_main__":
    print("Module hold GameScene class")