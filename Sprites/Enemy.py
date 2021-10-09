import pygame
from uuid import uuid4
from random import randint
from Sprites.Player import PlayerData
import Core.utility as util
from Sprites.SpriteData.EnemyData import EnemyData
from config import FLOOR, SCREEN_HEIGHT, SCREEN_WIDTH


# list of availible sprites with stats
sprite_list = [
    { "name": "hunk",        "hp": 30,       "attack": 10,  "speed": 7 },   # 0, common
    { "name": "bitch",       "hp": 30,       "attack": 10,  "speed": 7 },   # 1, common
    { "name": "fancypants",  "hp": 0.1,      "attack": 5,   "speed": 6 },   # 2, rare and invicible (runs away)
    { "name": "arnold",      "hp": 150,      "attack": 30,  "speed": 8 },   # 3, boss
    { "name": "chuck",       "hp": 150,      "attack": 30,  "speed": 8 }    # 4, boss
]


class Enemy(pygame.sprite.Sprite):
    """ enemy sprite class, constructor require sprite index to create instance """

    # class constuctor
    def __init__(self, sprite_index):
        super().__init__()

        sprite = sprite_list[sprite_index]      # get sprite from sprite list


        # sprite stats 
        self.sprite_id      = uuid4()           # generate sprite id      
        self.sprite_index   = sprite_index      # set sprite index

        self.sprite_name    = sprite['name']    # set sprite name
        self.sprite_health  = sprite['hp']      # set sprite health
        self.sprite_attack  = sprite['attack']  # set sprite attack
        self.sprite_speed   = self._modify_speed(sprite['speed'])   # set sprite speed


        self.sprite_killed  = False             # true only for instance when sprite gets killed
        self.sprite_is_dead = False             # true if sprite is dead


        self.player_data        = PlayerData()  # intial player data object
        self.damage_to_player   = 0             # damage to player

        self.remove_timer       = 5             # timer for removing dead sprite


        # sprite images and animations
        self.image_stand            = util.get_sprite_surface(self.sprite_name, "stand")
        self.image_dead             = util.get_sprite_surface(self.sprite_name, "dead")
    
        self.animation_walk_left    = util.get_sprite_surface(self.sprite_name, "walk", 2)
        self.animation_walk_right   = util.flip_image_list(self.animation_walk_left)

        self.animation_attack_left  = util.get_sprite_surface(self.sprite_name, "attack", 3)
        self.animation_attack_right = util.flip_image_list(self.animation_attack_left)

        self.animation_damage_left  = util.get_sprite_surface(self.sprite_name, "damage", 2)
        self.animation_damage_right = util.flip_image_list(self.animation_damage_left)


        # initalized image and rect
        self.image  = self.image_stand
        self.rect   = self.image.get_rect(midbottom = (SCREEN_WIDTH + 50, FLOOR - 10))


        # animation and logic values
        self.freeze_count   = 0         # a count down index for disabled sprite

        self.orient_left    = False     # orient sprite to left if true

        self.walk_active    = False     # true when walk animation active
        self.walk_index     = 0         # index for walk animation

        self.attack_active  = False     # true when attack animation active
        self.attack_index   = 0         # index for attack animation

        self.damage_active  = False     # true when taking damage animation active
        self.damage_index   = 0         # index for taking damage animation


        # play sound effect on boss spawn
        if sprite_index == 3: util.play_sound_effect("arnold_spawn", 1)
        if sprite_index == 4: util.play_sound_effect("chuck_spawn",  1)


    # update sprite with player input
    def update(self, player_data):
        
        self.destroy()              # run destroy first

        self.sprite_killed = False  # reset sprite killed
        self.damage_to_player = 0   # and attack result

        self.handle_input_data(player_data)     # handle player data

        self.handle_attack()        # handle attack
        self.handle_walk()          # handle walk

        self.handle_animation()     # handle animation

        return self.export_data()   # export sprite data to game scene


    # destroy sprite if dead
    def destroy(self):
        """ destroys sprite if dead and remove timer ran out"""

        if not self.sprite_is_dead: return      # return if sprite is not dead

        self.remove_timer -= 0.1                # decrement remove timer
        if self.remove_timer < 0: self.kill()   # kill sprite if timer ran out


    # handle input player data
    def handle_input_data(self, player_data):
        """ handle player input data """

        if self.sprite_is_dead: return  # return if sprite is dead

        self.player_data = player_data  # store player_data in object


        # itterate damage report
        for damage in player_data.damage_report:

            if self.sprite_id == damage.sprite_id:      # if id match
                self.sprite_health  -= damage.damage    # subract damage from health
                self.damage_active  = True              # activate damage animation

                # set different behaviour for fancypants
                if self.sprite_index == 2:
                    util.play_sound_effect("fancypants_run")    # play runaway crying for fancypants
                    return

                util.play_random_punch_effect()         # play random punch effect
                self.no_move        = 2                 # set no move counter


    # handle attack logic
    def handle_attack(self):
        """ handle attack logic for sprite"""

        if self._sprite_disabled(): return  # return if sprite disabled

        if self._player_in_attack_range():  # if player in attackrange
            self.attack_active = True       # attack player

    
    # handle walk logic
    def handle_walk(self):
        """ handle walk logic for sprite"""

        if self._sprite_disabled(): return  # return if sprite disabled

        to_left = self.rect.centerx > self.player_data.x_pos    # check if player is left of sprite
        dist = abs(self.rect.centerx - self.player_data.x_pos)  # get distance between sprites

        # move left
        if to_left and dist > 100:              # if to left and distance to large
            self.rect.x -= self.sprite_speed    # move left
            self.orient_left = True             # orient left
            self.walk_active = True             # activate walk
            return

        # move left backwards
        if to_left and dist < 50:               # if to left and distance to small
            self.rect.x += self.sprite_speed    # move right
            self.orient_left = True             # orient left
            self.walk_active = True             # activate walk
            return

        # move right
        if not to_left and dist > 100:          # if to right and distance to large
            self.rect.x += self.sprite_speed    # move right
            self.orient_left = False            # orient right
            self.walk_active = True             # activate walk
            return

        # move left backwards
        if not to_left and dist < 50:           # if to right and distance to small
            self.rect.x -= self.sprite_speed    # move right
            self.orient_left = False            # orient right
            self.walk_active = True             # activate walk
            return
        
        self.walk_active = False    # return not walking if none above valid


    # handle animations
    def handle_animation(self):
        """ handle image to rect for animation. Decide animation in hierarchical order """

        # animate dead if sprite is dead
        if self.sprite_is_dead:

            # default for all except fancypants
            if self.sprite_index != 2:
                self.image = self.image_dead
                return
            
            # set death for fancypants
            self._handle_fancypants_death()
            return

        # animate stand if player is dead
        if self.player_data.is_dead:
            self.image = self.image_stand
            return

        # handle damage animation first
        if self.damage_active:
            self._handle_damage_animation()
            return

        # handle sprite freeze here
        if self.freeze_count > 0:
            self.image = self.image_stand
            self.freeze_count -= 0.1


        # then attack animation
        if self.attack_active:
            self._handle_attack_animation()
            return

        # and last walk animation
        if self.walk_active:
            self._handle_walk_animation()
            return
        
        # animate stand if this pont reached
        self.image = self.image_stand


        pass


    # export sprite data
    def export_data(self):
        """ export sprite data for game scene"""
        
        # create data object
        data = EnemyData()

        # populate object fields
        data.id                 = self.sprite_id
        data.x_pos              = self.rect.centerx
        data.damage_to_player   = self.damage_to_player
        data.is_dead            = self.sprite_is_dead
        data.sprite_killed      = self.sprite_killed
        data.kill_bonus         = 0

        # set sprite kill bonus if sprite is killed
        if self.sprite_killed:
            if self.sprite_index == 0: data.kill_bonus = 1
            if self.sprite_index == 1: data.kill_bonus = 2
        
        return data


    # modify sprite speed
    def _modify_speed(self, speed):
        """ """
        modifier = speed + (randint(-30, 30) / 100)
        return int(modifier)
    

    # check if sprite is is disabled
    def _sprite_disabled(self):
        """ return true if sprite is disabled """
        if self.freeze_count > 0:   return True     # true if freeze count active
        if self.attack_active:      return True     # true if attack active
        if self.damage_active:      return True     # true if damage active
        if self.sprite_is_dead:     return True     # true if sprite is dead

        return False


    # resolve if player is in attack range
    def _player_in_attack_range(self):
        """ return true if player is within attack range of sprite """


        if self.player_data.y_pos != FLOOR: return False    # False if player in air

        dist = abs(self.rect.centerx - self.player_data.x_pos)  # distance between player and sprite

        return (dist >= 50 and dist <= 100)     # True if distance between 50 and 100
 

    # handle walk animation
    def _handle_walk_animation(self):
        """ handle image for walk animations """
        
        # get animation group from orientation
        image_group = self.animation_walk_left if self.orient_left else self.animation_walk_right

        # increment animation index
        self.walk_index += 0.2

        # secure index in range
        if self.walk_index > len(image_group):
            self.walk_index = 0
        
        # set image
        self.image = image_group[int(self.walk_index)]
        

    # handle attack animation and resolve attack
    def _handle_attack_animation(self):
        """ handle images and attack animations and resolve attack damage"""

        # set animation group
        image_group = self.animation_attack_left if self.orient_left else self.animation_attack_right

        # itterate animation index
        self.attack_index += 0.2

        # secure index range and resolve attack damage if index ends
        if self.attack_index > len(image_group):

            self.attack_index = 0       # reset attack index
            self.attack_active = False  # disable attack animation
            self.freeze_count = 1.5

            # set player damage if playuer in range
            if self._player_in_attack_range():
                self.damage_to_player = self.sprite_attack
            
            return  # and return from loop
        
        # set image from image group
        self.image = image_group[int(self.attack_index)]


    # handle damage animation and assess damage
    def _handle_damage_animation(self):
        """ handle image for damage animation and assess damage on sprite """

        # fancypants damage handled differently
        if self.sprite_index == 2:
            self.sprite_is_dead = True
            self.sprite_killed = True
            return
        
        # image group
        image_group = self.animation_damage_left if self.orient_left else self.animation_damage_right

        # itterate animation index
        self.damage_index += 0.2

        # secure index in range and assess damage if index end
        if self.damage_index > len(image_group):

            self.damage_index   = 0         # reset animation index
            self.damage_active  = False     # deactivate animation

            self._assess_sprite_damage()    # assess sprite damage
            return                          # return 
        
        # update image for animation
        self.image = image_group[int(self.damage_index)]


    # assess sprite damage
    def _assess_sprite_damage(self):
        
        if self.sprite_health > 0: return   # return if sprite has health

        self.sprite_is_dead = True      # set sprite dead
        self.sprite_killed  = True      # report sprite killed
        self.image = self.image_dead    # set image as dead


        # correct sprite dead pos
        x_pos = self.rect.centerx
        y_pos = SCREEN_HEIGHT - 20
        self.rect = self.image.get_rect(midbottom = (x_pos, y_pos))


    # handle fancypanys runaway animation
    def _handle_fancypants_death(self):
        
        # increment walk animation
        self.walk_index += 0.2

        # secure index not out of range
        if  self.walk_index > len(self.animation_damage_left):
            self.walk_index = 0
        
        # set image for animation
        self.image = self.animation_damage_left[int(self.walk_index)]

        # set x axis
        self.rect.x += 12

        # remove if out of sceen
        if self.rect.x > SCREEN_WIDTH + 100:
            self.kill()


if __name__ == "__main__":
    print("Module hold fancy pants")