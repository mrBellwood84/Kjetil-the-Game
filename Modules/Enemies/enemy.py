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

class Enemy(pygame.sprite.Sprite):

    def __init__(self, sprite_index):
        super().__init__()

        # game settings
        self.settings = GameSettings()


        # stats and settings
        self.sprite_index   = sprite_index
        self.sprite_name    = sprite_list[sprite_index]

        self.sprite_speed   = 6

        self.player_x_pos = 0


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
        self.walk_block         = False
        self.attack_animation   = False
        self.damage_animation   = False

        self.dead_animation     = False     # true if enemy is dead, block other animations

        self.animation_index    = 0         # index for all animation


    # handle walk toward player
    # also ensure player is dead animation
    def handle_walk(self):

        # stop any walk if sprite is dead
        if self.dead_animation:
            self.image = self.sprite_dead
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
        
        # move right
        if not to_left and self.rect.right < self.player_x_pos and not self.walk_block:
            self.rect.x += self.sprite_speed
            self.walk_animation = True
            return
        
        # if this point reached, turn of walk animation
        self.walk_animation = False

    # handle attack
    def handle_attack(self):
        pass

    # handle death
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
            self.animation_index += 0.2

            # secure index
            if self.animation_index > len(group):
                self.animation_index = 0
            
            # adjust image and return
            self.image = group[int(self.animation_index)]
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