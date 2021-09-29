

# player report for sprite
class PlayerReport:

    def __init__(self, position, damage_reports = []):

        self.pos            = position          # hold player position
        self.damage_report  = damage_reports    # hold damage report for sprites


# damage report for sprite
class DamageReport:

    def __init__(self, sprite_id, damage):
        self.sprite_id  = sprite_id         # hold sprite id
        self.damage     = damage            # hold damage to sprite