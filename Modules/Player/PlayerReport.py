

# player report for sprite
class PlayerReport:

    def __init__(self, position, damage_reports, health, shit, sperm, player_dead, shoot, direction):


        self.pos            = position          # hold player position
        self.damage_report  = damage_reports    # hold damage report for sprites

        self.health         = health            # hold health data for gui
        self.shit           = shit              # hold shit bonus data
        self.sperm          = sperm             # hold sperm bonus data

        self.shoot          = shoot             # shoot projectile
        self.direction      = direction         # direction of projectile, true = left

        self.player_dead    = player_dead
        


# damage report for sprite
class DamageReport:

    def __init__(self, sprite_id, damage):
        self.sprite_id  = sprite_id         # hold sprite id
        self.damage     = damage            # hold damage to sprite