import settings
from random import randint


class Player:

    def __init__(self, player_id, name, ws):
        self._id = player_id
        self._name = name
        self._ws = ws
        self.alive = False
    def new_game(self,color):
        self.alive = True
        self.color = color
        self.attack = []
    def add_region(self,p):
        self.region.append(p)
    def set_attack(self, x, y):
        self.attack = [x,y]
        print(self.attack)
    def get_id(self):
        return self._id
        
    def get_attack(self, world):
        return self.attack
        
    def get_ws(self):
        return self._ws
        