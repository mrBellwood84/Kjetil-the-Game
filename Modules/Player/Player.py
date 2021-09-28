from resource_manager import flip_surface_list, get_sprite_surface
from Modules.settings import GameSettings
import pygame

'''
Player sprite
'''
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # Game settings
        self.settings = GameSettings()


        # Player stats and settings

        self.player_health  = 200
        self.player_attack  = 15


        self.player_speed   = 8
        self.player_gravity = 0

        # Graphics and animation collection
        self.player_stand               = get_sprite_surface("jantheman", "stand")
        self.player_jump                = get_sprite_surface("jantheman", "jump")
        self.player_damage              = get_sprite_surface('jantheman', 'damage')

        self.player_walk_right          = get_sprite_surface("jantheman", "walk", 2)
        self.player_walk_left           = flip_surface_list(self.player_walk_right)
        self.player_walk_index          = 0

        self.player_slap_attact_right   = get_sprite_surface("jantheman", "slap", 3)
        self.player_slap_attact_left    = flip_surface_list(self.player_slap_attact_right)

        self.player_cock_attack_right   = get_sprite_surface("jantheman", "cock", 4)
        self.player_cock_attack_left    = flip_surface_list(self.player_cock_attack_right)

        self.player_ass_attack_right    = get_sprite_surface("jantheman", 'ass', 2)
        self.player_ass_attack_left     = flip_surface_list(self.player_ass_attack_right)


        # Initial player image and rectanggle
        self.image  = self.player_stand
        self.rect   = self.image.get_rect(bottom = self.settings.floor)


        # Animation values

        self.orient_left            = False     # hold orientation for animations

        self.walk_animation         = False     # true if player walk
        self.jump_animation         = False     # true if player jump

        self.attack_animation       = False     # true if player execute any attack
                                                # used to block walk animation when attack is executed

        self.active_slap_attack     = False     # true if slap attack active
        self.active_ass_attack      = False     # true if ass attack active
        self.active_cock_attack     = False     # true if cock attack active

        self.attack_animation_index = 0         # hold attack animation index

        self.damage_animation       = False
        self.damage_animation_timer = 0


    # handle player walk
    def handle_walk(self):

        if self.damage_animation: return

        # get keys
        keys = pygame.key.get_pressed()

        # handle walk right
        if (keys[pygame.K_d] and self.rect.right < self.settings.screen_width):
            self.rect.x += self.player_speed
            self.walk_animation = True
            self.orient_left    = False

        # handle walk left
        elif (keys[pygame.K_a] and self.rect.left > 0):
            self.rect.x -= self.player_speed
            self.walk_animation = True
            self.orient_left    = True
        
        # handle no walk
        else:
            self.walk_animation = False
    

    # handle player jump
    def handle_jump(self):

        if self.damage_animation: return

        # handle jump input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == self.settings.floor:
            self.player_gravity = -20
            self.jump_animation = True

        # handle gravity pull
        if self.player_gravity != 0 or self.rect.bottom != self.settings.floor:
            self.player_gravity += 1
            self.rect.y += self.player_gravity

            # stop gravity if player reach floor
            if self.rect.bottom >= self.settings.floor:
                self.rect.bottom = self.settings.floor
                self.player_gravity = 0
                self.jump_animation = False


    # handle player walk and jump animation
    def handle_move_animations(self):
        
        # disable movement animation if acitve attack
        if self.attack_animation or self.damage_animation: return

        # handle jump only if active
        if self.jump_animation:
            self.image = self.player_jump
            return
        
        # handle walk animation
        if self.walk_animation:
            # set animation group
            group = self.player_walk_left if self.orient_left else self.player_walk_right

            # increment animation index
            self.player_walk_index += 0.2

            # secure index 
            if self.player_walk_index > len(group):
                self.player_walk_index = 0
            
            # adjust image and return
            self.image = group[int(self.player_walk_index)]
            return
        
        # set standing if no above is valid
        self.image = self.player_stand


    # handle attack
    def handle_attack(self):
        
        if self.damage_animation: return

        #abort if attack is already executed
        if self.attack_animation: return

        # get keys
        keys = pygame.key.get_pressed()

        # check slap attack
        if keys[pygame.K_s]:
            self.attack_animation   = True
            self.active_slap_attack = True
            return

        # check ass attack
        if keys[pygame.K_e]:        
            self.attack_animation   = True
            self.active_ass_attack  = True
            return

        # check cock attack
        if keys[pygame.K_q]:
            self.attack_animation   = True
            self.active_cock_attack = True
            return


    # handle player damage
    def handle_player_damage(self, damage):

        if self.damage_animation:
            self.damage_animation_timer -= 0.1
            if self.damage_animation_timer <= 0:
                self.damage_animation = False
            self.image = self.player_damage


        if damage == 0: return
        
        self.player_health -= damage
        self.damage_animation = True
        self.damage_animation_timer = 1
        print(self.player_health)

    # handle attack animation
    def handle_attack_animation(self):
        
        # return if no active attack
        if not self.attack_animation: return

        # handle slap attack
        if self.active_slap_attack:

            # get attack direction group
            group = self.player_slap_attact_left if self.orient_left else self.player_slap_attact_right
            
            # increment animation index
            self.attack_animation_index += 0.2

            # deactive attack if attack complete
            if self.attack_animation_index > len(group):
                self.attack_animation_index = 0
                self.active_slap_attack = False
                return
            
            # update image and return
            self.image = group[int(self.attack_animation_index)]
            return

        # handle ass attack
        if self.active_ass_attack:

            # get attack direction group
            group = self.player_ass_attack_left if self.orient_left else self.player_ass_attack_right
            
            # increment animation index
            self.attack_animation_index += 0.2

            # deactive attack if attack complete
            if self.attack_animation_index > len(group):
                self.attack_animation_index = 0
                self.active_ass_attack = False
                return
            
            # update image and return
            self.image = group[int(self.attack_animation_index)]
            return

        # handle cock attack
        if self.active_cock_attack:

            # get attack direction group
            group = self.player_cock_attack_left if self.orient_left else self.player_cock_attack_right
            
            # increment animation index
            self.attack_animation_index += 0.4

            # deactive attack if attack complete
            if self.attack_animation_index > len(group):
                self.attack_animation_index = 0
                self.active_cock_attack = False
                return
            
            # update image and return
            self.image = group[int(self.attack_animation_index)]
            return
        
        # deactivate attack animations if none active
        self.attack_animation = False


    # return player center x pos
    def player_x_center(self):
        # return given player rect with equal 60
        return self.rect.centerx

    # update sprite
    def update(self, damage):

        # handle movement
        self.handle_walk()
        self.handle_jump()
        self.handle_player_damage(damage)
        self.handle_move_animations()

        # handle attack
        self.handle_attack()
        self.handle_attack_animation()