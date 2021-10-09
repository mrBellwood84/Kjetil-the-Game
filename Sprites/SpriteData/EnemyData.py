#   enemy sprite data is returned from the update method and appended to list in scene
#   it contain id and position for player attack resolutions, damage given to player,
#   reports if sprite is dead, and give player kill bonus

class EnemyData:

    def __init__(self):

        self.id                 = None      # id of enemy sprite

        self.x_pos              = 0         # center x of enemy rect

        self.damage_to_player   = 0         # damage to player

        self.is_dead            = False     # sprite is dead
        
        self.sprite_killed      = False     # true for instance when sprite is killed

        self.kill_bonus         = 0         # bonus given to player when killed
        """ 
            Bonus returned when killed by player:
                0: none
                1: shit bonus
                2: cum bonus
                3: health bonus
        """


if __name__ == "__main__":
    print("Module hold EnemyData class")