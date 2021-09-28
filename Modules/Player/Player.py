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

        self.player_health  = 200   # player health
        self.player_attack  = 15    # player attack damage

        self.is_dead = True         # game end when this is true


        self.player_speed   = 8     # player speed
        self.player_gravity = 0     # gravity for jump


        # Graphics and animation collection
        self.player_standing            = get_sprite_surface("jantheman", "stand")
        self.player_jumping             = get_sprite_surface("jantheman", "jump")
        self.player_damaged             = [get_sprite_surface('jantheman', 'damage'), get_sprite_surface('jantheman', 'damage') ]

        self.player_walk_right          = get_sprite_surface("jantheman", "walk", 2)
        self.player_walk_left           = flip_surface_list(self.player_walk_right)

        self.player_slap_attact_right   = get_sprite_surface("jantheman", "slap", 3)
        self.player_slap_attact_left    = flip_surface_list(self.player_slap_attact_right)

        self.player_cock_attack_right   = get_sprite_surface("jantheman", "cock", 4)
        self.player_cock_attack_left    = flip_surface_list(self.player_cock_attack_right)

        self.player_ass_attack_right    = get_sprite_surface("jantheman", 'ass', 2)
        self.player_ass_attack_left     = flip_surface_list(self.player_ass_attack_right)


        # Initial player image and rectanggle
        self.image  = self.player_stand
        self.rect   = self.image.get_rect(bottom = self.settings.floor)

        # variables for enemy interaction


        # other variables

        self.no_movement = False    # true when movement is blocked


        # Animation values

        self.orient_left            = False     # hold orientation for animations


        self.walk_animation         = False     # true if player walk
        self.walk_animation_index   = 0         # animation index for walking


        self.jump_animation         = False     # true if player jump


        self.active_slap_attack     = False     # true if slap attack active
        self.active_ass_attack      = False     # true if ass attack active
        self.active_cock_attack     = False     # true if cock attack active
        self.attack_animation_index = 0         # hold attack animation index


        self.damage_animation       = False     # true if player gets damaged
        self.damage_animation_index = 0         # index for damage animation


        self.sperm_explode_animation    = False     # true if sperm exlpode
        self.shit_explode_animation     = False     # true if shit explode
        self.explotion_animation_index  = 0         # index for explosion animation


    # handle player walk
    def handle_walk(self):

        # stop if movement is blocked
        if self.no_movement: return

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

        if self.no_movement: return

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


    # handle attack
    def handle_attack(self):
        
        # block attack if no mvement order
        if self.no_movement: return

        # get keys
        keys = pygame.key.get_pressed()

        # check slap attack
        if keys[pygame.K_s]:
            self.no_movement        = True
            self.active_slap_attack = True
            return

        # check ass attack
        if keys[pygame.K_e]:
            self.no_movement        = True
            self.active_ass_attack  = True
            return
        
        # check cock attack
        if keys[pygame.K_q]:
            self.no_movement        = True
            self.active_cock_attack = True
            return


    # handle player walk and jump animation
    def handle_move_animations(self):
        
        # disable movement animation if acitve attack
        if self.no_movement: return

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


    # handle attack animation and result
    def handle_attack_and_damage_animations(self):
        
        #DEV :: continue here

        # check dead
        # check damage
        # check and resolve attacks
            # face closes enemy for any attack
            # all enemies in range get damaged

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
        self.a = False


    # handle player damage
    def handle_player_damage(self, damage):

    # update sprite
    def update(self, damage):

        # clear attack resoluton
        # handle game inputs
        # handle user inputs
        # handle animations
        # return object with:
            # position
            # attack resolutions


        # handle inputs
        self.handle_walk()
        self.handle_jump()
        self.handle_attack()

        # self.handle_player_damage(damage)
        self.handle_move_animations()

        # handle animations
        self.handle_move_animations()
        self.handle_attack_animation()