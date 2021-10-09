#   the player data gets returned from the update method at set as variable in the scene class
#   the enemy sprites will use coordinates to decide behaviors and check for damage in damagereport
#   the status fields are used to update the player stats gui
#   if the projectile field is populated, the projectile object will be added in the sprite group

class PlayerData:
    """ player data to be exported to scene class"""

    def __init__(self):

        self.x_pos  = 0     # hold center x position for player sprite
        self.y_pos  = 0     # hold bottom y position for player sprite

        self.damage_report  = []        # hold successfull damage reports from attacks

        self.health         = 0         # hold health status
        self.cum_bonus      = 0         # hold cum bonus status
        self.shit_bonus     = 0         # hold shit bonus status

        self.projectile     = None      # contain projectile for shooting

        self.is_dead        = False     # set true if player is dead

if __name__ == "__main__":
    print("Module hold PlayerData class")