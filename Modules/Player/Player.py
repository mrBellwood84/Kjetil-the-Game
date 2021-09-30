from Modules.Player.PlayerReport import DamageReport, PlayerReport
from resource_manager import flip_surface_list, get_sprite_surface, play_random_hit_sound, play_sound_effect
from Modules.settings import GameSettings
import pygame
from random import choice


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

        self.sperm_bonus    = 0     # hold sperm
        self.shit_bonus     = 0     # hold shit

        self.is_dead = False        # game end when this is true

        self.player_speed   = 8     # player speed
        self.player_gravity = 0     # gravity for jump


        self.attack_resolutions = []        # hold attack resolutions for player
        self.enemies_report     = []        # hold enemies report
        self.shooting           = None      # 0 = cum, 1 = shit,
        
        self.death_sound_effect = False     # Turn true when play sound effect


        # Graphics and animation collection
        self.player_standing            = get_sprite_surface("jantheman", "stand")
        self.player_jumping             = get_sprite_surface("jantheman", "jump")

        self.player_damaged             = get_sprite_surface("jantheman","damage",2)

        self.player_walk_right          = get_sprite_surface("jantheman", "walk", 2)
        self.player_walk_left           = flip_surface_list(self.player_walk_right)

        self.player_slap_attact_right   = get_sprite_surface("jantheman", "slap", 3)
        self.player_slap_attact_left    = flip_surface_list(self.player_slap_attact_right)

        self.player_cock_attack_right   = get_sprite_surface("jantheman", "cock", 4)
        self.player_cock_attack_left    = flip_surface_list(self.player_cock_attack_right)

        self.player_ass_attack_right    = get_sprite_surface("jantheman", 'ass', 3)
        self.player_ass_attack_left     = flip_surface_list(self.player_ass_attack_right)

        self.sperm_explode              = get_sprite_surface("jantheman", 'sperm', 5)
        self.shit_explode               = get_sprite_surface("jantheman", "shit", 6)  


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
        self.explosion_animation_index  = 0         # index for explosion animation


    # handle input data
    def handle_input_data(self, input_data):

        self.enemies_report = input_data        # store input data

        # handle player damage
        for report in input_data:


            if report.kill_bonus == 1:
                self.shit_bonus += 0.26
            if report.kill_bonus == 2:
                self.sperm_bonus += 0.26
            
            if self.shit_bonus >= 2:
                self.player_health = 0
                self.damage_animation = True
                self.shit_explode_animation = True
                self.no_movement = True
                if not self.death_sound_effect:
                    play_sound_effect("ass_explode")
                    self.death_sound_effect = True
                return
            
            if self.sperm_bonus >= 2:
                self.player_health = 0
                self.damage_animation = True
                self.sperm_explode_animation = True
                self.no_movement = True
                if not self.death_sound_effect:
                    play_sound_effect("cock_explode")
                    self.death_sound_effect = True
                return


            if report.damage != None:
                self.player_health      -= report.damage    # subtract damage from health
                self.damage_animation   = True              # set damage animation as true
                self.no_movement        = True              # set no movement as true
            
            if self.player_health <= 0:
                self.shit_explode_animation = True
                if not self.death_sound_effect:
                    play_sound_effect("player_death")
                    self.death_sound_effect = True


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

        if self.is_dead: return

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


    # orient attack toward closest enemy
    def _orient_attack_direction(self):

        if self.enemies_report == []: return        # return if no enemy reports

        closest = self.settings.screen_width        # set inital closest to screen widht

        for enemy in self.enemies_report:           # loop enemy list

            dist = abs(self.rect.centerx - enemy.pos)   # check distance to enemy

            if closest > dist:      # if enemy is closer

                self.orient_left = True if (self.rect.centerx > enemy.pos) else False    # check if enemy is to the right of player
                closest = dist                  # set new closest distance


    # handle attack
    def handle_attack(self):
        
        # block attack if no mvement order
        if self.no_movement: return

        self._orient_attack_direction()

        # get keys
        keys = pygame.key.get_pressed()

        # check slap attack
        if keys[pygame.K_s]:
            self.no_movement        = True
            self.active_slap_attack = True
            return

        # check ass attack
        if keys[pygame.K_e]:
            if self.shit_bonus < 1 or self.jump_animation: return      # disable ass if shit not loaded or player jumping

            self.shit_bonus -= 1                # subtract shit from colon
            self.no_movement        = True      # block other stuff
            self.active_ass_attack  = True      # activate ass blast animation
            play_sound_effect("ass")           # play sound effect
            return
        
        # check cock attack
        if keys[pygame.K_q]:
            if self.sperm_bonus < 1 or self.jump_animation: return     # disable attack if cock not loaded or player jumping

            self.sperm_bonus -= 1               # subtract power from cock
            self.no_movement        = True      # block other stuff
            self.active_cock_attack = True      # activate cock attack animation
            play_sound_effect("cock")
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


    # resolve slap attack
    def _resolve_slap_attack(self):
        
        for enemy in self.enemies_report:
            
            in_range = False
            is_left = self.rect.centerx > enemy.pos

            if is_left and self.orient_left:
                dist = self.rect.centerx - enemy.pos
                if dist > 50 and dist < 80:
                    in_range = True
            
            if not is_left and not self.orient_left:
                dist = enemy.pos - self.rect.centerx
                if dist > 50 and dist < 80:
                    in_range = True

            if in_range:
                play_random_hit_sound()
                report = DamageReport(enemy.id, self.player_attack)
                self.attack_resolutions.append(report)


    # handle attack animation and attack result
    def handle_attack_and_damage_animations(self):

        # check dead
        if self.is_dead: return
        

        # check damage
        if self.damage_animation:

            # check and run shit explosion animation
            if self.shit_explode_animation:
                
                # iterate animation index
                self.explosion_animation_index += 0.2

                if self.explosion_animation_index > len(self.shit_explode):
                    self.is_dead        = True
                    self.no_movement    = True
                    return

                # set image
                self.image = self.shit_explode[int(self.explosion_animation_index)]
                return


            # check and run ass explosion animation
            if self.sperm_explode_animation:

                # iterate animation index
                self.explosion_animation_index += 0.2

                if self.explosion_animation_index > len(self.sperm_explode):
                    self.is_dead        = True
                    self.no_movement    = True
                    return

                # set image
                self.image = self.sperm_explode[int(self.explosion_animation_index)]
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
                self._resolve_slap_attack()
            
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
                self.shooting               = 1
            
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
                self.shooting               = 0
            
            # update image and return
            self.image = group[int(self.attack_animation_index)]
            return

    # create player report
    def create_player_report(self):
        return PlayerReport(self.rect.centerx, self.attack_resolutions, self.player_health, self.shit_bonus, self.sperm_bonus, self.is_dead, self.shooting, self.orient_left)


    # update sprite
    def update(self, input_data):

        self.attack_resolutions = []                # clear attack resolutons
        self.shooting           = None              # clear shooting value

        self.handle_input_data(input_data)          # handle input data

        self.handle_attack()                        # handle attack inputs
        self.handle_jump()                          # handle jump input
        self.handle_walk()                          # handle move inputs

        self.handle_attack_and_damage_animations()  # handle attack animations
        self.handle_move_animations()               # handle move animations

        return self.create_player_report()

