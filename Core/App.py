# This module hold the application class

import pygame, sys, config, time
from pygame.locals import *
from Core.AppStore import AppStore


class App:
    """ Create and run application window """

    def __init__(self):

        # intialize pygame
        pygame.init()

        # create storage for global variables
        App.Store = AppStore()

        # intialize screen
        size = config.SCREEN_WIDTH, config.SCREEN_HEIGHT            # create size tuple
        pygame.display.set_caption(config.SCREEN_TITLE)             # set screen 
        screen = pygame.display.set_mode(size, config.SCREEN_FLAG)  # create screen based on size and flag
        App.SCREEN = screen                                         # set screen as application field

        # set game clock
        App.CLOCK  = pygame.time.Clock()   # game clock
        App.FPS    = config.FPS            # set FPS tick

        # Scene dict
        App.scenes          = {}        # dict
        App.active_scene    = None      # keyword for active scene


    # run mehtod for running application
    def run(self):
        """ run game mainloop """

        # this is the gameloop
        while True:

            print(App.active_scene)
            
            # check events
            for event in pygame.event.get():
                
                # check quit event and stop loop if false
                if event.type == pygame.QUIT:
                    break
            
            # break loop if no active scene
            if App.active_scene == None:
                print("no active scene")
                break

            scene = App.scenes[App.active_scene]()  # create instance of scene class
            scene.run()                             # run scene


        # quit pygame and clean exit if loop ends
        pygame.quit()   # clean pygame exit
        sys.exit()      # clean system exit

    
    # append scene to list
    def add_scene(App, key, scene):
        App.scenes[key] = scene
    

    # set active scene key
    def set_active_scene(App, key):
        App.active_scene = key
    

# execute this print if running this script
if __name__ == '__main__':

    print("Module hold Application class")