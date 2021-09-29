
class EnemyReport:

    def __init__(self, id, pos, damage, killed):
        self.id     = id        # hold sprite id
        self.pos    = pos       # hold sprite pos
        self.damage = damage    # hold damage given to player
        self.killed = killed    # true when sprite gets killed