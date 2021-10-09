## Hold shared functions for application

import pygame                   # import pygame
from os.path import join        # import join from os path
import paths                    # import local app paths
from random import randint      # import random integer


# get single surface from resource folder with filename
def get_surface(path, filename):
    """ 
        Get a png file from path and filename and return as pygame image. 

        Note that ".png" is added as file postfix and should not be added to filename string.

        Params:
            path (string): Path to recource folder
            
            filename (string): Filename

        Return:
            pygame.image
    """

    # complete filename
    filename += ".png"
    # get image path
    image_path = join(path, filename)
    # return pygame image object
    return pygame.image.load(image_path).convert_alpha()


# get sprite surfaces from resource folder
def get_sprite_surface(sprite_name, filename, group = 0):
    """
        Get sprite images from resource sprite folder. Set group number to import image list for animation.

        See Resource documentation for image convention

        Params:
            sprite_name (string): name of sprite / foldername

            filename (string): name of image / animation name

            group (int): number of images in animation

        Return:
            pygame.image || list with pygame.image
    """

    # get path
    path = join(paths.sprite_dir, sprite_name)

    # return single image
    if group == 0:
        return get_surface(path, filename)
    
    # image list
    image_list = []

    # get images
    for x in range(group):
        file_num = x + 1                            # get file number
        file = filename + f'_{file_num}'            # add file number to file name
        image_list.append(get_surface(path, file))  # append image to list
    
    # return file name
    return image_list


# invert surface
def flip_image(image):
    """
        Flip a pygame image on the x axis.

        Params:
            image (pygame.image)

        Return:
            pygame.image
    """

    return pygame.transform.flip(image, True, False)


# invert surface list
def flip_image_list(image_list):
    """ 
        Flip a list of pygame images

        Params:
            image_list (list): list with pygame.image objects

        Return:
            list, pygame.image objects
    """

    # return a list of flipped images
    return [ flip_image(x) for x in image_list]


# play sound effect
def play_sound_effect(effect_name, volume = 0.5):
    """
        Get .ogg file and plays sound effect once.

        Params:
            effect_name (string): name of ogg sound file

            volume (float): set sound volume between 0 and 1

            loop (bool): runs in foreverloop if true

        Return: void
    """

    # get file name and file path
    file = f'{effect_name}.ogg' 
    path = join(paths.sound_effect_dir, file)

    # create soundobject, set volume and play
    sound  = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()


# play random hit sound effect
def play_random_punch_effect():
    """
        Plays a random sound effect from soundeffects/hits
    """

    effect = randint(1,18)              # pick random effect
    path = join("punch", str(effect))   # create path for play_sound_effect function

    # play sound with play sound effect function
    play_sound_effect(path, 0.3)



if __name__ == "__main__":
    print("Module hold shared functions for application")
