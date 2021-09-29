from Modules.Player.PlayerReport import PlayerReport
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

        self.is_dead = False        # game end when this is true

        self.player_speed   = 8     # player speed
        self.player_gravity = 0     # gravity for jump


        self.attack_resolutions = []    # hold attack resolutions for player
        self.enemies_report     = []    # hold enemies report


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

        self.sperm_explode  = []
        self.shit_explode = []


        # Initial player image and rectanggle
        self.image  = self.player_standing
        self.rect   = self.image.get_rect(bottom = self.settings.floor)


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


    # handle input data
    def handle_input_data(self, input_data):

        self.enemies_report = input_data        # store input data

        # handle player damage
        for report in input_data:
            if report.damage != None:
                self.player_health      -= report.damage    # subtract damage from health
                self.damage_animation   = True              # set damage animation as true
                self.no_movement        = True              # set no movement as true
                print("health:", self.player_health)


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

        # handle jump input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == self.settings.floor:
            print("jump")
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
            print("face closest enemy function here")
            return

        # check ass attack
        if keys[pygame.K_e]:
            self.no_movement        = True
            self.active_ass_attack  = True
            print("face closest enemy function here")
            return
        
        # check cock attack
        if keys[pygame.K_q]:
            self.no_movement        = True
            self.active_cock_attack = True
            print("face closest enemy function here")
            return


    # handle player walk and jump animation
    def handle_move_animations(self):
        
        # disable movement animation if acitve attack
        if self.no_movement: return

        # handle jump only if active
        if self.jump_animation:
            self.image = self.player_jumping
            return
        
        # handle walk animation
        if self.walk_animation:
            # set animation group
            group = self.player_walk_left if self.orient_left else self.player_walk_right

            # increment animation index
            self.walk_animation_index += 0.2

            # secure index 
            if self.walk_animation_index > len(group):
                self.walk_animation_index = 0
            
            # adjust image and return
            self.image = group[int(self.walk_animation_index)]
            return
        
        # set standing if no above is valid
        self.image = self.player_standing

    # handle attack animation and attack result
    def handle_attack_and_damage_animations(self):
        

        # check dead
        if self.is_dead:
            self.image = self.player_jumping
            print("DEBUG: Player dead animation missing")
            return
        

        # check damage
        if self.damage_animation:

            # check and run shit explosion animation
            if self.shit_explode_animation:
                print("DEBUG: Shit explode animation missing")
                # set is dead
                return

            # check and run ass explosion animation
            if self.sperm_explode_animation:
                print("Debug: Sperm explode")
                # set is dead
                return
            
            # iterate damage animation index
            self.damage_animation_index += 0.2

            # secure animation index
            if self.damage_animation_index > len(self.player_damaged):
                self.damage_animation_index = 0
                self.damage_animation = False
                self.no_movement = False
            
            # set image
            self.image = self.player_damaged[int(self.damage_animation_index)]
            return


        # check slap attack
        if self.active_slap_attack:

            # get attack direction group
            group = self.player_slap_attact_left if self.orient_left else self.player_slap_attact_right
            
            # increment animation index
            self.attack_animation_index += 0.2

            # deactive attack if attack complete
            if self.attack_animation_index > len(group):

                self.attack_animation_index = 0
                self.active_slap_attack     = False
                self.no_movement            = False
                print("resolve slap attack here")
            
            # update image and return
            self.image = group[int(self.attack_animation_index)]
            return


        # check ass attack
        if self.active_ass_attack:

            # get attack direction group
            group = self.player_ass_attack_left if self.orient_left else self.player_ass_attack_right
            
            # increment animation index
            self.attack_animation_index += 0.2

            # deactive attack if attack complete
            if self.attack_animation_index > len(group):

                self.attack_animation_index = 0
                self.active_ass_attack      = False
                self.no_movement            = False
                print("shoot shit here")
            
            # update image and return
            self.image = group[int(self.attack_animation_index)]
            return


        # check cock attack
        if self.active_cock_attack:

            # get attack direction group
            group = self.player_cock_attack_left if self.orient_left else self.player_cock_attack_right
            
            # increment animation index
            self.attack_animation_index += 0.4

            # deactive attack if attack complete
            if self.attack_animation_index > len(group):

                self.attack_animation_index = 0
                self.active_cock_attack     = False
                self.no_movement            = False
                print("shoot sperm here")
            
            # update image and return
            self.image = group[int(self.attack_animation_index)]
            return

    # create player report
    def create_player_report(self):
        return PlayerReport(self.rect.centerx, self.attack_resolutions)




    # update sprite
    def update(self, input_data):

        self.attack_resolutions = []                # clear attack resolutons

        self.handle_input_data(input_data)          # handle input data

        self.handle_attack()                        # handle attack inputs
        self.handle_jump()                          # handle jump input
        self.handle_walk()                          # handle move inputs

        self.handle_attack_and_damage_animations()  # handle attack animations
        self.handle_move_animations()               # handle move animations

        return self.create_player_report()

