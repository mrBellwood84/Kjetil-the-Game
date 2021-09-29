
class EnemyReport:

    def __init__(self, id, pos, damage, killed, kill_bonus):
        self.id     = id        # hold sprite id
        self.pos    = pos       # hold sprite pos
        self.damage = damage    # hold damage given to player
        self.killed = killed    # true when sprite gets killed
    
        self.kill_bonus = kill_bonus     # any bonus for kills given here
            # 0 : No bonus
            # 1 : Shit bonus
            # 2 : Sperm bonus