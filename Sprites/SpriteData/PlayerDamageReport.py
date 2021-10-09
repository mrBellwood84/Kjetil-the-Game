# the damage report contain information about sucessfull attack from player
# enemy sprites will check damage report and subract from health

class PlayerDamageReport:
    """ hold player damage report to resolve enemy damage"""

    def __init__(self, sprite_id, damage):

        self.sprite_id  = sprite_id     # id for enemy attacked
        self.damage     = damage        # damage value


if __name__ == "__main__":
    print("Module hold PlayerDamageReport class")