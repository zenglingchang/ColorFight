
from player import Player
from random import randint
Direction = [[-1,0], [0,-1], [1,0], [0,1]]
class AI(Player):
    def __init__(self, player_id, name):
        self._id = player_id
        self._name = name
        self.alive = False
        self.isAI = True
        
    def set_attack(self, attack, world):
        i = randint(0,3)
        if not attack:
            self._attack = [self._home[0] + Direction[i][0], self._home[1] + Direction[i][1]]
        else:
            self._attack[0] = attack[0] + Direction[i][0]
            self._attack[1] = attack[1] + Direction[i][1]
        return 