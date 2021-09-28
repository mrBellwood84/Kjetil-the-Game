from resource_manager import flip_surface_list, get_sprite_surface
from Modules.settings import GameSettings
import pygame

# sprite list
sprite_list = [
    "hunk",         # 0, common
    "bitch",        # 1, common
    "fancypants",   # 2, rare
    "arnold",       # 3, boss
    "chuck",        # 4, boss
]

sprites_health = [
    30,     # hunk
    30,     # bitch
    1000,   # fancypants
    300,    # arnold
    500     # chuck
]

sprites_attack = [
    5,      # hunk
    3,      # bitch
    1,      # fancypants
    10,     # arnold
    20,     # chuck
]

class Enemy(pygame.sprite.Sprite):

    def __init__(self, sprite_index):
        super().__init__()

        # game settings
        self.settings = GameSettings()


        # stats and settings
        self.sprite_index   = sprite_index
        self.sprite_name    = sprite_list[sprite_index]


        # stats for health and attacj
        self.sprite_health  = sprites_health[sprite_index]
        self.sprite_attack  = sprites_attack[sprite_index]

        self.sprite_speed       = 4

        self.walk_block         = False
        self.walk_block_timer   = 0

        self.attack_block       = False
        self.attack_block_timer = 0

        self.attack_result  = None 
        self.player_x_pos   = 0           # hold player center x


        # Graphics and animation
        self.sprite_stand           = get_sprite_surface(self.sprite_name, "stand")
        self.sprite_dead            = get_sprite_surface(self.sprite_name, "dead")

        self.sprite_walk_left       = get_sprite_surface(self.sprite_name,"walk",2)
        self.sprite_walk_right      = flip_surface_list(self.sprite_walk_left)

        self.sprite_attack_left     = get_sprite_surface(self.sprite_name, "attack", 3)
        self.sprite_attack_right    = flip_surface_list(self.sprite_attack_left)

        self.sprite_damage_left     = get_sprite_surface(self.sprite_name, "damage", 2)
        self.sprite_damage_right    = flip_surface_list(self.sprite_damage_left)



        # initial image and rect
        self.image  = self.sprite_stand
        self.rect   = self.image.get_rect(midbottom = (self.settings.screen_width - 200 , self.settings.floor - 10))


        # animation values
        self.orient_left        = False     # hold orientation for walk or attack
        
        self.walk_animation     = False
        self.attack_animation   = False
        self.damage_animation   = False

        self.dead_animation     = False     # true if enemy is dead, block other animations

        self.walk_animation_index       = 0     # index for walk animation
        self.attack_animation_index     = 0     # index for attack animaton


    # handle walk toward player
    # also ensure player is dead animation
    def handle_walk(self):

        # stop any walk if sprite is dead
        if self.dead_animation:
            self.image = self.sprite_dead
            return
        
        # handle walkblock
        if self.walk_block:
            self.walk_block_timer -= 0.1
            if self.walk_block_timer <= 0:
                self.walk_block = False
            return
        

        # check if player is left of sprite
        to_left = self.rect.centerx > self.player_x_pos
        # update animation boolean
        self.orient_left = True if to_left else False

        # move left
        if to_left and self.rect.left > self.player_x_pos and not self.walk_block:
            self.rect.x -= self.sprite_speed
            self.walk_animation = True
            return

        # move backward right
        if to_left and not self.walk_block and (self.rect.centerx - self.player_x_pos) < 55:
            self.rect.x += self.sprite_speed
            self.walk_animation = True
            return
        
        # move right
        if not to_left and self.rect.right < self.player_x_pos and not self.walk_block:
            self.rect.x += self.sprite_speed
            self.walk_animation = True
            return
        
        # move backward left
        if not to_left and not self.walk_block and (self.player_x_pos - self.rect.centerx) < 55:
            self.rect.x -= self.sprite_speed
            self.walk_animation = True
            return
        
        # if this point reached, turn of walk animation
        self.walk_animation = False

    # resolves executed attacj
    def resolve_attack(self):

        self.attack_block = True        # set timeout for next attack
        self.attack_block_timer = 10    # set timer for countdown

        in_range = False

        is_left = self.rect.centerx > self.player_x_pos   # get player direction

        # check if player is in reach left
        if is_left and self.orient_left:
            dist = self.rect.centerx - self.player_x_pos
            if dist > 50 and dist < 80:
                in_range = True
        
        # check if player is in reach right
        if not is_left and not self.orient_left:
            dist =  self.player_x_pos - self.rect.centerx
            if dist > 50 and dist < 80:
                in_range = True
        
        # if player was in reach, set result at sprite attack value
        if in_range: return self.sprite_attack


    # handle attack
    def handle_attack(self):

        self.attack_result = None

        # return if sprite is dead
        if self.dead_animation: return
        
        # check if attack is blocked
        if self.attack_block:
            self.attack_block_timer -= 1
            if self.attack_block_timer <= 0:
                self.attack_block = False
            return

        # check if player in reach
        player_distance = abs(self.player_x_pos - self.rect.centerx)
        in_reach = player_distance <= 70 and player_distance >= 50     

        if in_reach:
            self.walk_block = True
            self.walk_block_timer = 1
            self.attack_animation = True
            


    # handle damage / death
    def handle_damage(self):
        pass

    # handle all animation
    def handle_animations(self):
        
        # abort if player is dead
        if self.dead_animation: return

        # walk animation
        if self.walk_animation and not self.walk_block:

            # get animation group
            group = self.sprite_walk_left if self.orient_left else self.sprite_walk_right

            # increment walk animation
            self.walk_animation_index += 0.2

            # secure index
            if self.walk_animation_index > len(group):
                self.walk_animation_index = 0
            
            # adjust image and return
            self.image = group[int(self.walk_animation_index)]
            return

        # attack animation and attack resolve
        if self.attack_animation and not self.attack_block:
            
            # get animation group
            group = self.sprite_attack_left if self.orient_left else self.sprite_attack_right

            # incerement attack animation index
            self.attack_animation_index += 0.2

            # secure attack index
            if self.attack_animation_index > len(group):
                self.attack_animation_index = 0                 # reset attack index
                self.attack_animation: False                    # cancel attack animation
                self.attack_result = self.resolve_attack()      # resolve attack
            self.image = group[int(self.attack_animation_index)]
            return

        self.image = self.sprite_stand


    #update position data
    def update_position_data(self, player_pos):
        self.player_x_pos = player_pos


    #update sprite
    def update(self, player_pos):

        self.handle_walk()
        self.handle_attack()
        self.handle_damage()
        self.handle_animations()

        self.update_position_data(player_pos)

        return self.attack_result