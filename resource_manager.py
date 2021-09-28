import os
import pygame


# hold relative path sprite folder
__sprite_path = os.path.join("Resources", "Sprites")


# adds image postfix and get image file as converted pygame surface
def __get_surface(path, filename):

    # add postfix
    filename += ".png"

    # create path
    image_path = os.path.join(path, filename)

    # return pygame surface
    return pygame.image.load(image_path).convert_alpha()


# Sprite import
def get_sprite_surface(sprite_name, filename, group=0):
    """
    Get images for sprite animation. Use image name minus file postfix.
    
    Return single surface if no group specified.

    Set group amount if enumerated images are to be imported as list

    If error occurs, check folder and naming convention.
    """

    # get common path
    path = os.path.join(__sprite_path, sprite_name)

    # if no group, return single
    if group == 0:
        return __get_surface(path, filename)

    else:
        # create result list
        image_group = []

        # populate result list with surfaces
        for x in range(group):
            index = x+1
            file = filename + f'_{index}'
            image_group.append(__get_surface(path, file))

        # return list
        return image_group


# invert surface
def flip_surface(surface):
    """
    Flips the surface on the x axis
    """

    return pygame.transform.flip(surface, True, False)


# invert surface list
def flip_surface_list(surface_list):
    """
    Flips a list of surfaces on the x axis
    """

    # # create result list
    result = []

    # add flipped surfaces to result list
    for surface in surface_list:
        flipped = flip_surface(surface)
        result.append(flipped)
    
    # return result
    return result