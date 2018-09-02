from random import randint

class Player:

    def __init__(self, player_id, name, ws):
        self._id = player_id
        self._name = name
        self._ws = ws
        self.alive = False
        self.isAI = False
        self.observation = []
        self.choose = -1
        self.score = 0
        self.cost = 0
        
    def tra_observation(self, world, attacklist):
        observation = [[[1 if x[0]==self._id else 0, 1 if x[0]>0 else 0, x[1], x[2]] for x in line ] for line in world]
        for p in attacklist:
            attack = attacklist[p]
            if attack:
                observation[attack[0]][attack[1]][3] = -20
        return observation
        
    def set_observation(self, world):
        self.observation = self.tra_observation(world,[])
        
    def new_game(self,color, home):
        self.alive = True
        self.color = color
        self._attack = []
        self._home = home
        
    def set_attack(self, x, y):
        self._attack = [x,y]
        
    def get_name(self):
        return self._name
        
    def get_id(self):
        return self._id
        
    def get_attack(self):
        self.cost = 0
        return self._attack
        
    def get_ws(self):
        return self._ws
    
    async def send_message(self, commands):
        if not self.isAI:
            await self._ws.send_str(commands)