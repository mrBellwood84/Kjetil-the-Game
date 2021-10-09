import pygame
from pygame.locals import *
import Core.utility as util
from Sprites.Projectile import Projectile
from Sprites.SpriteData.PlayerDamageReport import PlayerDamageReport
from Sprites.SpriteData.PlayerData import PlayerData
from config import FLOOR, SCREEN_WIDTH


class Player(pygame.sprite.Sprite):
    """ class for player sprite """


    def __init__(self):
        super().__init__()


        # player stats and settings
        self.player_health  = 200           # player health / hitpoints
        self.player_attack  =  15           # player attack damage
        self.player_speed   =   8           # player movement speed

        self.player_gravity =   0           # player gravity (activted when jumping)

        self.cum_bonus      =   0           # accumelated cum for special attack
        self.shit_bonus     =   0           # accumelated diahrrea for special attack

        self.projectile     = None          # contain projectile if created

        self.enemy_data     =  []           # hold list of data returned from enemy sprites
        self.damage_report  =  []           # hold list of damage reports

        self.player_is_dead     = False     # true when player is dead


        # player image and animation groups
        self.image_standing         = util.get_sprite_surface("jantheman","stand")
        self.image_jumping          = util.get_sprite_surface("jantheman","jump")

        self.animation_damage_right = util.get_sprite_surface("jantheman", "damage", 2)
        self.animation_damage_left  = util.flip_image_list(self.animation_damage_right)

        self.animation_walk_right   = util.get_sprite_surface("jantheman","walk",2)
        self.animation_walk_left    = util.flip_image_list(self.animation_walk_right)
        
        self.animation_attack_right = util.get_sprite_surface("jantheman","slap",3)
        self.animation_attack_left  = util.flip_image_list(self.animation_attack_right)

        self.animation_ass_right    = util.get_sprite_surface("jantheman","ass", 3)
        self.animation_ass_left     = util.flip_image_list(self.animation_ass_right)

        self.animation_cock_right   = util.get_sprite_surface("jantheman","cock", 4)
        self.animation_cock_left    = util.flip_image_list(self.animation_cock_right)

        self.animation_cum_explode  = util.get_sprite_surface("jantheman","cum", 5)
        self.animation_shit_explode = util.get_sprite_surface("jantheman","shit", 6)

        
        # initial image and rectangle
        self.image  = self.image_standing
        self.rect   = self.image.get_rect(bottom = FLOOR)


        # animation variables
        self.no_walk        = False             # block walk input
        self.no_attack      = False             # block attack input
        self.no_jump        = False             # block jump input
        self.orient_left    = False             # orient animation direction

        self.walk_active    = False             # true when player walk
        self.walk_index     = 0                 # index for walk animation

        self.jump_active    = False             # true when player jump

        self.attack_active  = False             # true when player attack
        self.ass_active     = False             # true when player ass attack
        self.cock_active    = False             # true when player cock attack
        self.attack_index   = 0                 # animation index for attacks

        self.damage_active          = False     # true when player takes damage
        self.shit_explode_active    = False     # true when player shit explode
        self.cum_explode_active     = False     # true when player cum explode
        self.damage_index           = 0         # animation index for explosion


    # update player object
    def update(self, enemy_data):

        self.projectile     = None      # reset projectile field
        self.damage_report  = []

        self.handle_input_data(enemy_data)  # handle input data

        self.handle_user_input()    # handle user inputs
        self.handle_gravity()       # handle game gravity
        self.handle_animations()    # handle animations

        return self.export_data()


    # handle user input
    def handle_user_input(self):
        """ Method handle and control user inputs based on availible actions """

        if self.player_is_dead: return              # return if player is dead

        keys = pygame.key.get_pressed()             # get pressed keys

        if not self.no_attack:                      # handle attack inputs first

            self._handle_ass_attack_input(keys)     # handle ass and cock attack first
            self._handle_cock_attack_input(keys)    # so they don't get blocked by slap attack
            self._handle_slap_attack_input(keys)    # handle slap attack last

        if not self.no_jump: self._handle_jump_input(keys)  # handle jump input

        if not self.no_walk: self._handle_walk_input(keys)  # handle walk input


    # handle gravity
    def handle_gravity(self):
        ''' handles gravity logic for player sprite'''
        
        if not self.jump_active: return     # abort function if not jumping

        self.player_gravity += 1            # increment player gravity
        self.rect.y += self.player_gravity  # adjust player y position

        if self.rect.bottom >= FLOOR:       # if player at floor or lower

            self.rect.bottom = FLOOR        # set player at floor
            self.player_gravity = 0         # set gravity to 0

            self.jump_active = False        # disable jumping
            self.no_attack = False          # allow attack
            self.no_jump = False            # allow jump


    # handle animations
    def handle_animations(self):
        """ handles an animation logic"""
        
        if self.player_is_dead: return          # return if player is dead

        # handle animations in the following order
        if self.cum_explode_active:
            self._handle_cum_explosion_animation()
            return

        if self.shit_explode_active:
            self._handle_ass_explosion_animation()
            return

        if self.damage_active:
            self._handle_damage_animation()
            return

        if self.cock_active:
            self._handle_cock_attack_animation()
            return
        
        if self.ass_active:
            self._handle_ass_attack_animation()
            return

        if self.attack_active:
            self._handle_slap_attack_animation()
            return
        
        if self.jump_active:
            self.image = self.image_jumping
            return

        if self.walk_active:
            self._handle_walk_animation()
            return

        self.image = self.image_standing


    # handle walk input
    def _handle_walk_input(self, keys):
        ''' handle walk inputs '''

        # check key input
        no_pressed      = not keys[K_a] and not keys[K_d]   # check if any pressed
        both_pressed    = keys[K_a] and keys[K_d]           # check if both pressed

        if no_pressed or both_pressed:      # if both or none are pressed
            self.walk_active = False        # no walking
            return                          # return function

        # handle walk left
        if keys[K_a] and (self.rect.left > 0):         # walk left if not at screen border
            self.rect.x         -= self.player_speed    # increment left at player speed
            self.walk_active    = True                  # activate player walk animation
            self.orient_left    = True                  # orient player left

        # handle walk right
        if keys[K_d] and (self.rect.right < SCREEN_WIDTH):   # walk right if not at screen border
            self.rect.x         += self.player_speed    # increment right at player speed
            self.walk_active    = True                  # activate player walk animation
            self.orient_left    = False                 # orient player right


    # handle jump input
    def _handle_jump_input(self, keys):

        if keys[K_SPACE]:

            self.player_gravity -= 20       # execute jump

            self.no_jump        = True      # block jump
            self.no_attack      = True      # block attack
            self.jump_active    = True      # set jump as active


    # handle regular attack input
    def _handle_slap_attack_input(self, keys):
        """ handle slap attack """

        if keys[K_s]:
            self.attack_active = True   # activate attack

            self._resolve_attack_direction()    # resolve attack direction

            self.no_attack  = True     # block other attacks
            self.no_jump    = True     # block jumping
            self.no_walk    = True     # block walking


    # handle ass attack input
    def _handle_ass_attack_input(self, keys):
        """ handle ass special attack"""
        
        if self.shit_bonus < 1: return  # return if no brown torpedo loaded

        if keys[K_e]:
            self.ass_active     = True      # activate ass
            self.shit_bonus     -= 1        # extract from colon
            util.play_sound_effect("ass")   # play sound effect

            self._resolve_attack_direction()    # resolve attack direction

            self.no_attack  = True      # block other attacks
            self.no_jump    = True      # block jumping
            self.no_walk    = True      # block walking


    # handle cock attack input
    def _handle_cock_attack_input(self, keys):
        "handle cock special attack"
        
        if self.cum_bonus < 1: return   # return if cock not loaded

        if keys[K_q]:
            self.cock_active    = True      # activate cock
            self.cum_bonus      -=1         # extract cum from nutsack
            util.play_sound_effect("cock")  # play sound effect

            self._resolve_attack_direction()    # resolve attack direction

            self.no_attack  = True      # block other attacks
            self.no_jump    = True      # block jumping
            self.no_walk    = True      # block walking


    # handle walk animation
    def _handle_walk_animation(self):
        ''' handle walk animation in index'''

        # get image list according to orientation
        image_list = self.animation_walk_left if self.orient_left else self.animation_walk_right

        self.walk_index += 0.2                          # increment walk index
        if self.walk_index > len(image_list):           # secure index not out of range
            self.walk_index = 0     
        self.image = image_list[int(self.walk_index)]   # set sprite image

    
    # handle slap attack animation
    def _handle_slap_attack_animation(self):
        """ handle ass attack animation"""
        
        # get image group corresponding to attack direction
        image_group = self.animation_attack_left if self.orient_left else self.animation_attack_right

        self.attack_index += 0.2            # increment attack index

        if self.attack_index > len(image_group):    # if index ended
            self.attack_index   = 0                 # reset attack index
            self.attack_active  = False             # deactive attack

            self._resolve_attack_result()   # resolve attack

            self.no_attack  = False         # allow new attack
            self.no_jump    = False         # allow jump
            self.no_walk    = False         # allow walk
        
        # set sprite image
        self.image = image_group[int(self.attack_index)]


    # handle ass attack animation
    def _handle_ass_attack_animation(self):
        """ Handle ass attack animation """
        
        # get image group corresponding to attack direction
        image_group = self.animation_ass_left if self.orient_left else self.animation_ass_right

        self.attack_index += 0.2

        if self.attack_index > len(image_group):    # if index ended
            self.attack_index   = 0                 # reset attack index
            self.ass_active     = False             # deactive attack

            self._create_projectile("shit")         # create projectile

            self.no_attack  = False         # allow new attack
            self.no_jump    = False         # allow jump
            self.no_walk    = False         # allow walk
        
        # set sprite image
        self.image = image_group[int(self.attack_index)]


    # handle cock attack animation
    def _handle_cock_attack_animation(self):
        """ handle cock attack animation"""

        # get image group corresponding to attack direction
        image_group = self.animation_cock_left if self.orient_left else self.animation_cock_right

        self.attack_index += 0.2

        if self.attack_index > len(image_group):    # if index ended
            self.attack_index   = 0                 # reset attack index
            self.cock_active    = False             # deactive attack

            self._create_projectile("cum")   # resolve attack

            self.no_attack  = False         # allow new attack
            self.no_jump    = False         # allow jump
            self.no_walk    = False         # allow walk
        
        # set sprite image
        self.image = image_group[int(self.attack_index)]


    # handle damage animation
    def _handle_damage_animation(self):
        """ Handle damage animation """

        # get image group corresponding to direction
        image_group = self.animation_damage_left if self.orient_left else self.animation_damage_right

        self.damage_index += 0.2        # incement damage animation index

        if self.damage_index > len(image_group):
            self.damage_active = False  # deactivate damage animatoon
            self.damage_index = 0       # reset damange index

            self.no_walk    = False     # enable walk
            self.no_jump    = False     # enable jump
            self.no_attack  = False     # enable attack
        
        # set sprite image
        self.image = image_group[int(self.damage_index)]


    # handle cum explosion animation
    def _handle_cum_explosion_animation(self):
        """ handle cum explosion animation"""

        self.damage_index += 0.2    # increment damage index

        # if animation index runs out
        if self.damage_index > len(self.animation_cum_explode):
            # player is dead
            self.player_is_dead = True
            self.damage_index = 0
            return

        # set sprite image
        self.image = self.animation_cum_explode[int(self.damage_index)]


    # handle ass explosion animation
    def _handle_ass_explosion_animation(self):
        
        self.damage_index += 0.2    # increment damage index 

        # if animation index run out
        if self.damage_index > len(self.animation_shit_explode):
            # player is dead
            self.player_is_dead = True
            self.damage_index = 0
            return

        # set sprite image
        self.image = self.animation_shit_explode[int(self.damage_index)]

    
    # resolve attack direction
    def _resolve_attack_direction(self):
        """ resolve direction of attack based on the closest enemy"""

        if self.enemy_data == []: return    # return if no enemy report

        nearest = SCREEN_WIDTH              # initalize nearest as screen width

        # itterate enemy list
        for enemy in self.enemy_data:

            # get distance between sprites
            dist = abs(self.rect.centerx - enemy.x_pos)

            # if messured distance is smaller than current nearest
            if dist < nearest:

                # set orientation of attack toward enemy sprite
                self.orient_left = True if self.rect.centerx > enemy.x_pos else False

                # set nearest distance for next comparison
                nearest = dist


    # resolve player attack
    def _resolve_attack_result(self):
        """ resolves player attack toward enemy sprite"""

        # itterate enemy data objects
        for enemy in self.enemy_data:

            in_range = False                                # initalize in range as false
            is_left = self.rect.centerx > enemy.x_pos       # check if enemy is to left

            # if enemy to left and attack in that direction
            if is_left and self.orient_left:
                dist = self.rect.centerx - enemy.x_pos      # get distance
                if dist > 50 and dist < 100:                # and check attack range
                    in_range = True                         # report truth
            
            # if enemy to right and attack in that direction
            if not is_left and not self.orient_left:
                dist = enemy.x_pos - self.rect.centerx      # get distance
                if dist > 50 and dist < 100:                # and check attack range
                    in_range = True                         # report truth
            
            # if attack was in range
            if in_range:

                # create and store damage report
                report = PlayerDamageReport(enemy.id, self.player_attack)
                self.damage_report.append(report)

    
    # create projectile on special attack
    def _create_projectile(self, type):
        
        self._resolve_attack_direction()
        self.projectile = Projectile(type, self.rect.centerx, self.orient_left)
    

    # handle input data
    def handle_input_data(self, input_data):
        """ handle enemy data list """

        if self.player_is_dead: return      # return if player is dead
        
        self.enemy_data = input_data        # store enemy data

        for item in input_data:

            # only check killbonus if exist
            if item.kill_bonus > 0:

                if item.kill_bonus == 1:        # if getting shit bonus

                    self.shit_bonus += 0.26     # increment shit bonus
                    
                    if self.shit_bonus >= 2:    # if to much shit

                        if not self.shit_explode_active:                # if animation not active
                            util.play_sound_effect("ass_explode", 1)    # play soundeffect

                        self.shit_explode_active = True     # activate shit explosion

                        self.no_walk    = True      # disble walk
                        self.no_attack  = True      # disable attack
                        self.no_jump    = True      # disable jump


                        return              # and end function here
                
                if item.kill_bonus == 2:        # if getting cum bonus

                    self.cum_bonus += 0.26      # increment cum bonus

                    if self.cum_bonus >= 2:     # if to blue balls

                        if not self.cum_explode_active :                # if animation not active
                            util.play_sound_effect("cock_explode",1)    # play sound effect

                        self.cum_explode_active = True  # activate cum explosion

                        self.no_walk    = True  # disable walk
                        self.no_attack  = True  # disable attack
                        self.no_jump    = True  # disable jump


                        return      # end function here

            if item.damage_to_player > 0:   # if player get damaged
                
                # decrement player health
                self.player_health -= item.damage_to_player

                # explode player if health goes to zero or lower
                if self.player_health <= 0:
                    if not self.shit_explode_active:                # if animation not set
                        util.play_sound_effect("player_death",1)    # play sound effect
                    self.shit_explode_active = True                 # activate explode animation

                # else set damage animation
                else:
                    self.damage_active = True           # activate damage animation
                    util.play_random_punch_effect()     # play random punch effect

                                        # regarless
                self.no_walk    = True  # disable walk
                self.no_attack  = True  # disable attack
                self.no_jump    = True  # disable jump


    # export player data
    def export_data(self):
        """ export player data """

        data = PlayerData()

        data.x_pos          = self.rect.centerx
        data.y_pos          = self.rect.bottom

        data.damage_report  = self.damage_report

        data.health         = self.player_health
        data.cum_bonus      = self.cum_bonus
        data.shit_bonus     = self.shit_bonus

        data.projectile     = self.projectile

        data.is_dead        = self.player_is_dead

        return data
        


if __name__ == "__main__":
    print("Hold Player sprite class")