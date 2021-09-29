import pygame
from resource_manager import get_sprite_surface, flip_surface_list
from Modules.settings import GameSettings

projectile_types = [
    "cum",  # 0
    "shit"  # 1
]

class Projectile(pygame.sprite.Sprite):

    def __init__(self, type, x_cor, direction):
        super().__init__()

        # projectile stats and settings

        self.settings = GameSettings()

        self.speed      = 20     # projectile speed
        self.to_left    = not direction

        # get projectile type graphic
        self.projectile_left    = get_sprite_surface(projectile_types[type], projectile_types[type], 3)
        self.projectile_right   = flip_surface_list(self.projectile_left)

        # hold speed animation index
        self.animation_index = 0


        # initial image
        self.image = self.projectile_left[0] if self.to_left else self.projectile_right[0]

        # projectile rectangle
        self.rect  = self.image.get_rect(center = (x_cor, 500))
    

    def handle_movement(self):
        
        if self.to_left:
            self.rect.x += self.speed
            return
        self.rect.x -= self.speed

    def handle_animation(self):

        group = self.projectile_left if self.to_left else self.projectile_right
        
        # itterate animation
        self.animation_index += 0.3

        # secure animation
        if self.animation_index > len(group):
            self.animation_index = 0
        
        # animate
        self.image = group[int(self.animation_index)] 

    def update(self):

        self.handle_movement()
        self.handle_animation()
        self.destroy()

    # destroy if out of frame
    def destroy(self):
        if self.rect.x > self.settings.screen_width + 50 or self.rect.x < -50:
            self.kill()

