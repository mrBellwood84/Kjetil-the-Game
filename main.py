## Application start point

from Core.App import App
from Scenes.GameScene import GameScene
from Scenes.MenuScene import MenuScene


if __name__ == "__main__":

    app = App()                                 # Create instance for application

    app.add_scene("menu_scene", MenuScene)      # add menu scene
    app.add_scene("game_scene", GameScene)      # add game scene

    App.set_active_scene(App, "menu_scene")     # set menu scene as start scene

    app.run()                                   # run application
    

