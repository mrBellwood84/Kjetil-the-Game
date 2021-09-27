import os
import pygame

# path for Image folder
image_path = os.path.join("Resources","Images")

# import image file as pygame image
def get_JanTheMan(filename):
    path = os.path.join(image_path, "JanTheMan", filename)
    print(path)
    return pygame.image.load(path).convert_alpha()