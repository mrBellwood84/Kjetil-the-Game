from Core.App import App
from Core.utility import get_surface, play_sound_effect
from Scenes.GameScene import GameScene
from Scenes.assets import gamefont_title, gamefont_menu
from paths import image_dir, menu_music_path
import pygame
from pygame.locals import *
import sys


class MenuScene:
    ''' hold class for menu scene '''

    def __init__(self):
        
        self.show_help = False

        # set music and start play
        self.music = pygame.mixer.Sound(menu_music_path)
        self.music.set_volume(0.5)
        self.music.play(loops = -1)

        self.run_scene = True       # boolean for scene loop

    # draw menu
    def run(self): 

        while self.run_scene:

            for event in pygame.event.get():

                # manage quit event
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                # show instruction / help screen if H is pressed
                if event.type == KEYDOWN:
                    if event.key == K_h:
                        self.show_help = True
                    
                    # start game if SPACE is pressed
                    elif event.key == K_SPACE:
                        self.start_game()
                        pass

                    else:
                        self.show_help == False
            
            # show help if show help is true
            if self.show_help:
                self.instruction_screen()
            # else, show menu screen
            else:
                self.main_menu_screen()

            # update and tick
            pygame.display.update()
            App.CLOCK.tick(App.FPS)


    # draws main menu scene
    def main_menu_screen(self):

        # create title text
        title_text = gamefont_title.render('Kjetil, The Game', False, 'brown')
        title_rect = title_text.get_rect(center = (600,60))
        
        # get menu image
        kjetil_image = get_surface(image_dir, "kjetil")
        kjeti_rect = kjetil_image.get_rect(center=(600,220))

        # text for fresh start
        fresh = [
            "WELCOME",
            "Let's play a little game..."
        ]

        # text for image
        game_over = [
            "Game Over!!!",
            f"You teached {App.Store.sprites_killed} bitches and assholes a lesson!"
        ]

        # always show this text
        last = [
            "Press spacebar to start a new game!",
            "Hold \"H\" to read instructions."
        ]

        # list of text to screen
        txt_list = []

        # decide text to screen
        if App.Store.sprites_killed == 0:
            txt_list = fresh + last
        else:
            txt_list = game_over + last

        # create list with text for screen
        txt_images = [gamefont_menu.render(text, False, "brown") for text in txt_list]

        txt_rects   = []    # list for text rects
        y_pos       = 400   # y pos for text rects

        # create text rects
        for image in txt_images:
            txt_rects.append(image.get_rect(center=(600, y_pos)))
            y_pos += 50

        # fill screen with images
        App.SCREEN.fill((254,255,255))
        App.SCREEN.blit(title_text, title_rect)
        App.SCREEN.blit(kjetil_image, kjeti_rect)

        for index in range(4):
            App.SCREEN.blit(txt_images[index], txt_rects[index])

    # draw instruction screen
    def instruction_screen(self):

        # text for print
        text = [
            'Press "A" and "D" to move left and right.',
            'Press "SPACEBAR" to jump.',
            'Press "S" for a classic bitchslap to the face.',
            'Press "Q" for CumShot attack if your cock is loaded.', 
            'Press "E" for Assblast attack if your ass is loaded.',
            '',
            "You will be fighting hunkes and bitches, and sometimes a fancypants.",
            'Defeating a hunk will load up your ass with diarrhea.',
            "Defeating a bitch will load ip your cock with cum.",
            "Spraying a fancypants with diarrhea or cum will give you health.",
            "",
            'Be aware of your cumload and your shitload.', 
            'If load more than 1, you will explode!!!',
            "",
            "Oh, by the way:",
            "Chuck Norris or Arnold Schwarznegger might show up to kick your ass...",
            "",
            "Be like Kjetil, Be awesome!!!"
        ]

        # text images list
        lines = [gamefont_menu.render(t, False, 'brown') for t in text ]  
        
        rects = []  # populate text rects
        y_pos = 30  # get intial y pos for text

        # populate rect array
        for line in lines:
            rect = line.get_rect(midleft = (20, y_pos))
            rects.append(rect)
            y_pos += 30
        
        l = len(text)   # get length of text array

        # create background fill
        App.SCREEN.fill((254,255,255))

        # print text to screen
        for i in range(l):
            App.SCREEN.blit(lines[i], rects[i])

    # start game loop
    def start_game(self):

        self.run_scene = False                      # stop menu loop
        App.Store.sprites_killed = 0                # reset game score
        self.music.stop()                           # stop menu music
        play_sound_effect("start", 1)               # play start game sound effect
        App.set_active_scene(App, "game_scene")     # and set game scene as active scene

if __name__ == "__main__":
    print("Module hold MenuScene class")

