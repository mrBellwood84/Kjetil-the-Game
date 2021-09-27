from pygame import transform
from import_resource import get_JanTheMan
from pygame.constants import K_SPACE, K_d
from pygame.mixer import fadeout
from Modules.settings import GameSettings
import pygame
from pygame.draw import circle

'''
Player sprite
'''
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # Game settings
        self.settings = GameSettings()


        # Graphics
        self.player_standing = get_JanTheMan("jantheman_stand.png")
        self.player_jump = get_JanTheMan("jantheman_jump.png")

        self.player_walk = self.import_walk_animation()
        self.player_walk_index = 0

        self.player_slap_attact = self.import_slap_animation()
        self.player_slap_attact_index = 0

        self.player_ass_attack = self.import_ass_attack_animation()
        self.player_ass_attack_index = 0

        self.player_cock_attack = self.import_cock_animation()
        self.player_cock_attack_index = 0


        # Image and rect
        self.image = self.player_standing
        self.rect = self.image.get_rect(bottom = self.settings.floor)


        # physics
        self.speed = 5
        self.gravity = 0


        # animation booleans
        self.walk_animation = False
        self.jump_animation = False

        self.active_slap_attack = False
        self.active_cock_attack = False
        self.active_ass_attack  = False

        self.attack_active      = False
    

    # handle player walk
    def player_handle_walk(self):

        if self.attack_active: return

        # get keys pressed
        keys = pygame.key.get_pressed()

        # walk left
        if ((keys[pygame.K_LEFT] or keys[pygame.K_a])and self.rect.left > 0):
            self.rect.x -= self.speed
            self.walk_animation = True
        
        # walk right
        elif ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < self.settings.screen_width):
            self.rect.x += self.speed
            self.walk_animation = True

        else:
            self.walk_animation = False
    

    # handle player jump
    def player_handle_jump(self):

        # handle jump input
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.bottom == self.settings.floor:
            self.gravity = -20
            self.jump_animation = True

        # handle gravity pull
        if self.gravity != 0 or self.rect.bottom != self.settings.floor:
            self.gravity += 1
            self.rect.y += self.gravity

            # stop gravity if player reach floor
            if self.rect.bottom >= self.settings.floor:
                self.rect.bottom = self.settings.floor
                self.gravity = 0
                self.jump_animation = False


    # handle player movement animation
    def player_movement_animation(self):
        
        # abort if attack active
        if self.attack_active: return

        if self.jump_animation:
            self.image = self.player_jump
        elif self.walk_animation:
            self.player_walk_index += 0.2
            if self.player_walk_index > (len(self.player_walk)): 
                self.player_walk_index = 0
            self.image = self.player_walk[int(self.player_walk_index)]
        else:
            self.image = self.player_standing


    # handle player attack input
    def player_handle_attack(self):
        
        if not self.attack_active:

            keys = pygame.key.get_pressed()

            if (keys[K_SPACE]):
                self.attack_active = True
                self.active_slap_attack = True
            
            if (keys[pygame.K_q]):
                self.active_ass_attack = True
                self.attack_active = True
            
            if (keys[pygame.K_e]):
                self.active_cock_attack = True
                self.attack_active = True


    # handle attack animation
    def player_handle_attack_animation(self):

        # animate slap attack
        if self.active_slap_attack:
            self.player_slap_attact_index += 0.4
            if self.player_slap_attact_index > len(self.player_slap_attact):
                self.player_slap_attact_index = 0
                self.active_slap_attack = False
                self.attack_active = False
                return
            self.image = self.player_slap_attact[int(self.player_slap_attact_index)]
        
        # animate cock attack
        if self.active_cock_attack:
            self.player_cock_attack_index += 0.4
            if self.player_cock_attack_index > len(self.player_cock_attack):
                self.player_cock_attack_index = 0
                self.active_cock_attack = False
                self.attack_active = False
                return
            self.image = self.player_cock_attack[int(self.player_cock_attack_index)]
        
        # animate ass attack
        if self.active_ass_attack:
            self.player_ass_attack_index += 0.2
            if self.player_ass_attack_index > len(self.player_ass_attack):
                self.player_ass_attack_index = 0
                self.active_ass_attack = False
                self.attack_active = False
                return
            self.image = self.player_ass_attack[int(self.player_ass_attack_index)]


    # update sprite
    def update(self):
        self.player_handle_walk()
        self.player_handle_jump()
        self.player_movement_animation()

        self.player_handle_attack()
        self.player_handle_attack_animation()
    


    ### IMPORT METHODS ( for cleaner constructor ) ##

    # import walk animation images
    def import_walk_animation(self):
        walk_1 = get_JanTheMan("JanTheMan_walk_1.png")
        walk_2 = get_JanTheMan("jantheman_walk_2.png")

        return [walk_1, walk_2]
    
    # import slap attack animation images
    def import_slap_animation(self):
        slap_1 = get_JanTheMan("jantheman_slap_1.png")
        slap_2 = get_JanTheMan("jantheman_slap_2.png")
        slap_3 = get_JanTheMan("jantheman_slap_3.png")

        return [slap_1, slap_2, slap_3, slap_2, slap_1]

    # import cock attack animation images
    def import_cock_animation(self):
        cock_1 = get_JanTheMan("jantheman_ca_1.png")
        cock_2 = get_JanTheMan("jantheman_ca_2.png")
        cock_3 = get_JanTheMan("jantheman_ca_3.png")
        cock_4 = get_JanTheMan("jantheman_ca_4.png")

        return [cock_1, cock_2, cock_3, cock_4, cock_4, cock_4, cock_4,  cock_3, cock_2, cock_1]

    def import_ass_attack_animation(self):
        ass_1 = get_JanTheMan("jantheman_aa_1.png")
        ass_2 = get_JanTheMan("jantheman_aa_2.png")

        return [ass_1, ass_2, ass_2,ass_2, ass_1]