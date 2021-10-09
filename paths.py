## Hold paths for application resources and resource folders

from os.path import join

# image folder
image_dir = join("resources","images")

# sprite images folder
sprite_dir = join("resources","sprites")

# gamefont
font_path = join("resources","fonts","Pixeltype.ttf")

# sound effects folder
sound_effect_dir = join("resources","soundeffects")

# battle music
battle_music_path = join("resources","music","game_music.ogg")

# menu music
menu_music_path = join("resources","music","menu_music.ogg")

if __name__ == "__main__":
    print("Document hold pahts for resources and resource folders for application")