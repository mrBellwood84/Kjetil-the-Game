import pygame
from random import randint
import Core.utility as util
from config import SCREEN_WIDTH


class Projectile(pygame.sprite.Sprite):
    """ sprite class for projectiles. """

    def __init__(self, type, x_pos, to_left):
        super().__init__()
    
        # projectile stats and settings

        self.speed = 25 + (randint(-20, 20) / 10)   # set randomized speed
        self.to_left    = not to_left               # animation orientation

        # animation image lists and index
        self.projectile_right    = util.get_sprite_surface(type, type, 3)
        self.projectile_left   = util.flip_image_list(self.projectile_right)
        self.anim_index         = 0
        self.orient_left        = to_left

        # set image and rect
        self.image  = self.projectile_left[0] if self.to_left else self.projectile_right[0]
        self.rect   = self.image.get_rect(center = (x_pos, 520))

    # update projectile    
    def update(self):
        
        self.destroy()
        self.handle_move()
        self.handle_animation()
        
    # handle move
    def handle_move(self):
        """ moves projectile in oriented direction"""
        if self.to_left:
            self.rect.x += self.speed
            return
        self.rect.x -= self.speed


    # handle animation
    def handle_animation(self):
        """ handle animation for projectile """
        
        # get animation list
        image_list = self.projectile_left if self.orient_left else self.projectile_right

        # itterate animation index
        self.anim_index += 0.2

        # secure index range
        if self.anim_index > len(image_list):
            self.anim_index = 0
        
        # update image
        self.image = image_list[int(self.anim_index)]

    
    # destroy projectile if out of screen
    def destroy(self):
        if (self.rect.x < - 50) or (self.rect.x > SCREEN_WIDTH + 50):
            self.kill()

    
if __name__ == "__main__":
    print("Module hold Projectile sprite class")