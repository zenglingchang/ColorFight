from random import randint

class Player:

    def __init__(self, player_id, name, ws):
        self._id = player_id
        self._name = name
        self._ws = ws
        self.alive = False
        self.isAI = False
        
    def new_game(self,color, home):
        self.alive = True
        self.color = color
        self._attack = []
        self._home = home
        
    def set_attack(self, x, y):
        self._attack = [x,y]
        print(self._attack)
        
    def get_id(self):
        return self._id
        
    def get_attack(self):
        return self._attack
        
    def get_ws(self):
        return self._ws
    
    async def send_message(self, commands):
        if not self.isAI:
            await self._ws.send_str(commands)