from Modules.Enemies.EnemyReport import EnemyReport
from resource_manager import flip_surface_list, get_sprite_surface
from Modules.settings import GameSettings
import pygame, uuid

# sprite name list
sprite_list = [
    "hunk",         # 0, common
    "bitch",        # 1, common
    "fancypants",   # 2, rare
    "arnold",       # 3, boss
    "chuck",        # 4, boss
]

# sprite health list
sprites_health = [
    30,     # hunk
    30,     # bitch
    1000,   # fancypants
    150,    # arnold
    150     # chuck
]

# sprite attack power list
sprites_attack = [
    10,      # hunk
    8,      # bitch
    5,      # fancypants
    20,     # arnold
    20,     # chuck
]

sprite_speeds = [
    6,      # hunk
    8,      # bitch
    5,      # fancypants
    8,      # arnold
    8,      # chick
]


# class for enemy sprites
class Enemy(pygame.sprite.Sprite):

    def __init__(self, sprite_index):
        super().__init__()

        # game settings
        self.settings = GameSettings()


        # stats and settings
        self.sprite_id      = uuid.uuid4()                  # unique id for sprite
        self.sprite_index   = sprite_index                  # sprite index for lists and logic
        self.sprite_name    = sprite_list[sprite_index]     # sprite name tye

        self.sprite_health  = sprites_health[sprite_index]  # sprite health
        self.sprite_attack  = sprites_attack[sprite_index]  # sprite attack power

        self.sprite_speed   = sprite_speeds[sprite_index]   # sprite movement speed

        self.sprite_killed  = False     # True only for the instance when sprite gets killed
        self.sprite_is_dead = False     # True if sprite is dead
        self.player_is_dead = False     # True if player is dead


        # other stats

        self.attack_result  = None      # hold attack sendt to player      
        self.player_x_pos   = 0         # hold player center x

        self.no_move        = False     # halt sprite until timer runs out
        self.no_move_timer  = 0         # timer for no_move

        self.remove_timer   = 5         # remove timer


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
        self.rect   = self.image.get_rect(midbottom = (self.settings.screen_width + 50 , self.settings.floor - 10))


        # animation values
        self.orient_left        = False     # hold orientation for walk or attack
        
        self.walk_animation     = False     # true if sprite walk
        self.attack_animation   = False     # true if sprite attacks
        self.damage_animation   = False     # true if sprite get damaged

        self.walk_animation_index   = 0     # index for walk animation
        self.attack_animation_index = 0     # index for attack animaton
        self.damage_animation_index = 0     # index for damage animation



    # handle player inputs, includes death and damage
    def handle_input_data(self, input_data):

        self.player_x_pos = input_data.pos              # get player positon from report

        self.player_is_dead = input_data.player_dead        

        for damage in input_data.damage_report:

            if damage.sprite_id == self.sprite_id:
                self.sprite_health -= damage.damage
                self.no_move += 1
                self.damage_animation = True
        
        if self.sprite_health < 0:
            self.damage_animation = True


    # handle attack
    def handle_attack(self):

        # return if sprite has no move
        if self.no_move or self.sprite_is_dead or self.player_is_dead: return

        # excecute attack if player in range
        player_distance = abs(self.player_x_pos - self.rect.centerx)
        in_reach = player_distance in range(50, 80)

        if in_reach:
            self.no_move            = True      # disable movement
            self.no_move_timer      = 1         # set timer
            self.attack_animation   = True      # set attack animation


    # handle walk
    def handle_walk(self):

        if self.sprite_is_dead or self.player_is_dead: return      # return if sprite is dead

        # if no_move animation is active
        if self.no_move: 
            self.walk_animation = False     # secure no walk
            return                          # and return


        to_left = self.rect.centerx > self.player_x_pos     # check player to left
        self.orient_left = True if to_left else False       # update animation orientation

        # move left
        if to_left and self.rect.left > self.player_x_pos:
            self.rect.x -= self.sprite_speed
            self.walk_animation = True
            return

        # move backward right
        if to_left and (self.rect.centerx - self.player_x_pos) < 60:
            self.rect.x += self.sprite_speed
            self.walk_animation = True
            return
        
        # move right
        if not to_left and self.rect.right < self.player_x_pos:
            self.rect.x += self.sprite_speed
            self.walk_animation = True
            return
        
        # move backward left
        if not to_left and (self.player_x_pos - self.rect.centerx) < 60:
            self.rect.x -= self.sprite_speed
            self.walk_animation = True
            return
        
        self.walk_animation = False         # return no walk if this point reached


    # check damage to player (call when attack animation ends)
    def resolve_attack(self):
        
        in_range = False                                    # True if player was in range
        is_left = self.rect.centerx > self.player_x_pos     # get player direction from sprite


        # check if player is in reach left
        if is_left and self.orient_left:
            dist = self.rect.centerx - self.player_x_pos
            if dist in range(50, 80):
                in_range = True
        

        # check if player is in reach right
        if not is_left and not self.orient_left:
            dist =  self.player_x_pos - self.rect.centerx
            if dist in range(50, 80):
                in_range = True
        
                                                                # if attack was successful:
        if in_range: self.attack_result = self.sprite_attack    # set attack result
        

    # handle animations, include damage report
    def handle_animations(self):

        if self.sprite_is_dead:             # if sprite is dead
            self.remove_timer -= 0.1        # start remove timer

            if self.sprite_index == 2:  # special handle for sprite index 2

                # get animation group
                group = self.sprite_damage_left if self.orient_left else self.sprite_damage_right
                
                # increment index
                self.damage_animation_index += 0.3

                # secure index
                if self.damage_animation_index > len(group):
                    self.damage_animation_index = 0
                
                self.image = group[int(self.damage_animation_index)]
                self.rect.x += 12

                
            return                          # cancel all other animations


        # damage animation
        if self.damage_animation:

            # set special damage for sprite_2
            
            if self.sprite_index == 2:
                self.sprite_is_dead = True
                return

            # set animation group
            group = self.sprite_damage_left if self.orient_left else self.sprite_damage_right

            # increment animation index
            self.damage_animation_index += 0.2

            # secure animation index
            if self.damage_animation_index > len(group):

                self.damage_animation_index = 0
                self.damage_animation       = False

                # set sprite dead if sprite dies
                if self.sprite_health <= 0: 

                    self.sprite_killed = True           # set sprite killed for stat
                    self.sprite_is_dead = True          # set sprite is dead for stop any animation
                    self.image = self.sprite_dead       # set sprite dead image to rect
                    
                    # aligh corpse in screen
                    x_pos = self.rect.centerx
                    self.rect   = self.image.get_rect(midbottom = (x_pos, self.settings.screen_height - 20))
                    return
            
            self.image = group[int(self.damage_animation_index)]
            return
        

        # attack animation
        if self.attack_animation:

            # set animation group
            group = self.sprite_attack_left if self.orient_left else self.sprite_attack_right

            # increment animation index
            self.attack_animation_index += 0.2

            # secure animation index
            if self.attack_animation_index > len(group):

                self.attack_animation_index = 0
                self.attack_animation       = False
                self.resolve_attack()

            self.image = group[int(self.attack_animation_index)]
            return


        # walk animation
        if self.walk_animation:

            # get animation group
            group = self.sprite_walk_left if self.orient_left else self.sprite_walk_right

            # increment animation index
            self.walk_animation_index += 0.2

            # secure animation index
            if self.walk_animation_index > len(group):
                self.walk_animation_index = 0

            # set image
            self.image = group[int(self.walk_animation_index)]
            return


        # resolve nomove
        if self.no_move:
            self.no_move_timer -= 0.1
            if self.no_move_timer < 0:
                self.no_move = False

        # set stand animation
        self.image = self.sprite_stand


    # create sprite report
    def create_report(self):

        kill_bonus = 0
        if self.sprite_killed:
            if self.sprite_index == 0: kill_bonus = 1
            if self.sprite_index == 1: kill_bonus = 2

        # return sprite object for game loop
        return EnemyReport(self.sprite_id, self.rect.centerx, self.attack_result, self.sprite_killed, kill_bonus)


    #update sprite
    def update(self, input_data):

        self.destroy()  

        self.sprite_killed = False              # reset sprite killed value
        self.attack_result = None               # reset attack result

        self.handle_input_data(input_data)      # handle input data first
        self.handle_attack()                    # handle attack next
        self.handle_walk()                      # handle walk if last

        self.handle_animations()                # handle animation 
        return self.create_report()             # return report


    def destroy(self):
        if self.remove_timer <= 0:
            self.kill()