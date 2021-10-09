##  hold assets for application
#   in this case, only font objects 

from paths import font_path
import pygame

pygame.font.init()

gamefont_title      = pygame.font.Font(font_path, 72)   # large text for title
gamefont_status_bar = pygame.font.Font(font_path, 32)   #  font for status bars
gamefont_menu       = pygame.font.Font(font_path, 42)   #  font for status bars
gamefont_score_text = pygame.font.Font(font_path, 48)   #  for kill score

if __name__ == "__main__":
    print("Module hold game assets")