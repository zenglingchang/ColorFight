from player import Player
from random import randint
import pdb
from DeepQNetwork import DeepQNetwork

Direction = [[-1,0], [0,-1], [1,0], [0,1]]
DQN = DeepQNetwork()

class AI(Player):
    def __init__(self, player_id, name):
        self._id = player_id
        self._name = name
        self.alive = False
        self.isAI = True
        self.observation = []
        self.choose = -1
        self.score = 0
        
    def tra_observation(self, world, attacklist):
        observation = [[[1 if x[0]==self._id else 0, 1 if x[0]>0 else 0, x[1], x[2]] for x in line ] for line in world]
        for p in attacklist:
            attack = attacklist[p]
            if attack:
                observation[attack[0]][attack[1]][3] = 10
        return observation
        
    def set_observation(self, world):
        self.observation = self.tra_observation(world,[])
        
        
    def set_attack(self, attacklist, score, world):
        temp_observation = self.tra_observation(world,attacklist)
        if self.choose>=0:
            DQN.store_transition(self.observation, self.choose, score-self.score, temp_observation)
        attack = attacklist[self._id] if self._id in attacklist.keys() else None
        self.choose = DQN.Choose_action(temp_observation)
        self.score = score
        self.observation = temp_observation
        if self.choose == 4:
            return False
        if not attack:
            self._attack = [self._home[0] + Direction[self.choose][0], self._home[1] + Direction[self.choose][1]]
        else:
            self._attack[0] = attack[0] + Direction[self.choose][0]
            self._attack[1] = attack[1] + Direction[self.choose][1]
        return True