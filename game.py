from random import randint,choice
import json
import asyncio
import copy

import settings
from player import Player
from ai import AI

NameList = ["Bob", "Tom", "Candy", "Monkey", "Anna"]
_Nofun_ = 0
_Home_  = 20
_Defen_ = -5

class Game:

    def __init__(self):
        self._max_id = 0
        self._players = {}
        settings.InitColorList()
        self.running = False
        self._world = []
        self.count = 0

# Game logic Function :

    # The world is a three-dimensional array
        # Example: world[x][y] == [3,15] is means that \
            # the Point locating in (x,y) is belong to player_3 and it's value is 15 
    def new_world(self):
        temp =[copy.deepcopy([0,5,_Nofun_]) for i in range(settings.FIELD_SIZE_X)]
        self._world = [copy.deepcopy(temp) for i in range(settings.FIELD_SIZE_Y)]
                
    async def new_player(self, name, ws):
        self._max_id += 1
        player_id = self._max_id
        player = Player(player_id, name, ws)
        await self.send_personal(player, "SHAKE", player_id)
        self._players[player_id] = player
        if not settings.TRAN:
            self.count += 1
        return player
        
    def new_ai(self, name):
        self._max_id += 1
        player_id = self._max_id
        player = AI(player_id, name)
        self._players[player_id] = player
        self.count += 1
        
    def count_alive_players(self):
        return sum([int(p.alive) for p in self._players.values()])
        
    # The function will randomly generate one room and a color for each player 
    async def start_game(self):
        overlist = []
        for player in self._players.values():
            if player.isAI:
                overlist.append(player.get_id())
        for id in overlist:
            self.game_over(self._players[id])
        while self.count<4:
            self.new_ai(choice(NameList))
        await self.send_all("INIT")
        self.new_world()
        self.cur_attack = {}
        self.home = {}
        self.scorelist = {}
        colortemplist = []
        xytemplist = []
        for player in self._players.values():
            if settings.TRAN and not player.isAI:
                continue
            x = 0
            y = 0
            color = ""
            while 1:
                x = randint(0, settings.FIELD_SIZE_X - 1)
                y = randint(0, settings.FIELD_SIZE_Y - 1)
                flag = True
                for p in xytemplist:
                    if (x - p[0])**2 + (y - p[1])**2 < 5:
                        flag = False
                if flag == True:
                    xytemplist.append([x,y])
                    break
            while 1:
                color = choice(settings.kind_of_color)
                flag = True
                if color in colortemplist:
                    flag = False
                if flag == True:
                    colortemplist.append(color)
                    break
            player.new_game(color,[x,y])
            self.cur_attack[player.get_id()] = []
            self.home[player.get_id()] = [x, y]
            self.scorelist[player.get_id()] = 0
            await self.send_all("DRAWELEMENT", [settings.GetColor(color, settings.MAX_OCCUPY), x, y])
            await self.send_all("PLAYERVALUES",[player.get_id(),settings.GetColor(color, settings.MAX_OCCUPY),player.get_name(),player.color])
            self._world[x][y][0] = player.get_id()
            self._world[x][y][1] = settings.OCCUPY_VALUE*settings.COLOR_LEVEL*2
            self._world[x][y][2] = _Home_
        for player in self._players.values():
            if player.isAI:
                player.set_observation(self._world)
        print("number of alive :%d"%self.count_alive_players())
        
        
    # every region will reduced 1 value each frame
    # attck region will add 5 value each frame
    async def next_frame(self):
        renderlist = {}
        defencelist = []
        overlist=[]
        # Traverse all region where players are attacking
        for player in self._players.values():
            if not player.alive or (settings.TRAN and not player.isAI):
                continue
            player.cost -= 1
            point = self.cur_attack[player.get_id()]
            if not point:
                if player.isAI:
                    player.set_attack(self.cur_attack, self.scorelist[player.get_id()], self._world)
                self.filter_get_attack(player.get_id(), player.get_attack())
                continue
            region = self._world[point[0]][point[1]]
            if region[0] == player.get_id():
                if region[1] > settings.MAX_OCCUPY:
                    # Get AI action
                    if player.isAI and not player.set_attack(self.cur_attack, self.scorelist[player.get_id()], self._world):
                        self.Defence(player.get_id())
                        continue
                        
                    if self.filter_get_attack(player.get_id(), player.get_attack()):
                        self.RenderElement(renderlist, settings.GetColor(player.color, region[1]), point[0], point[1])
                else:
                    if region[2] == _Defen_:
                        region [1] += settings.OCCUPY_VALUE
                        self.RenderElement(renderlist, settings.GetColor(player.color, region[1]), point[0], point[1])
                        continue
                    region[1] = int(region[1]/settings.OCCUPY_VALUE + 1)*settings.OCCUPY_VALUE + settings.OCCUPY_VALUE
            else:
                if region[1] < 0 or region[0] == 0:
                    if region[2] == _Home_:
                        self.scorelist[player.get_id()] += int(self.scorelist[region[0]]/2) + 50
                        self.scorelist[region[0]] -= 100
                        overlist.append(region[0])
                        continue;
                    if region[0] != 0:
                        self.scorelist[region[0]] -= 3 if region[2] == _Defen_ else 1
                    self.scorelist[player.get_id()] += 2 if region[2] == _Defen_ else 1
                    if region[2] == _Defen_:
                        region[2] = _Nofun_
                    region[0] = player.get_id()
                    region[1] = settings.OCCUPY_VALUE
                else:
                    region[1] -= settings.OCCUPY_VALUE
                    self.RenderElement(renderlist, settings.GetColor(player.color, region[1]), point[0], point[1])
        # Reduce all region where player has occupied values
        for id in overlist:
            await self.game_over(self._players[id])
        for x in range(settings.FIELD_SIZE_X):
            for y in range(settings.FIELD_SIZE_Y):
                region = self._world[x][y]
                if region[0]!=0 and region[1]>=settings.OCCUPY_VALUE and region[2]!=_Home_:
                    if region[2] == _Defen_:
                        defencelist.append([x,y])
                        continue
                    region[1] -= 1
                    if settings.ColorChange(region[1]):
                        self.RenderElement(renderlist, settings.GetColor(self._players[region[0]].color,region[1]), x, y)

        # Send changes to each client 
        # print(self.cur_attack)
        for (color,points) in renderlist.items():
            await self.send_all("RENDER",[color,points])
        await self.send_all("DEFENCE",defencelist)
        await self.send_all("ATTACK",list(self.cur_attack.values()))
        await self.send_all("CREATEHOME",list(self.home.values()))
        for (id,score) in self.scorelist.items():
            await self.send_all("SCORE",[id,score])
            
        
    async def game_over(self, player):
        player.alive = False
        self.count -= 1
        if player.isAI:
            player.game_over(self.cur_attack, self.scorelist[player.get_id()], self._world)
        await self.send_all("PGAMEOVER",player.get_id())
        points = []
        for x in range(len(self._world)):
            for y in range(len(self._world[x])):
                if self._world[x][y][0] == player.get_id():
                    points.append([x,y])
                    self._world[x][y] = [0,5,_Nofun_]
        await self.send_all("RENDER",[settings.basecolor,points])
        del self.home[player.get_id()]
        del self.cur_attack[player.get_id()]
        del self.scorelist[player.get_id()]
        if player.isAI:
            await self.del_player(player)
        
    async def player_disconnected(self, player):
        player.ws = None
        if player.alive:
            render = await self.game_over(player)
            # self.apply_render(render)
            await self.del_player(player)
            
    async def del_player(self, player):
        del self._players[player._id]
        del player
# Assist Fuction :
    def GetRegion(self,point):
        return self._world[point[0]][point[1]]
    
    def MouseAttack(self, args):
        if not self._players[args[0]].alive:
            return
        self._players[args[0]].set_attack(args[1],args[2])
        
    def Defence(self,Id):
        if self.cur_attack[Id] and self.GetRegion(self.cur_attack[Id])[1] > settings.MAX_OCCUPY:
            region = self.GetRegion(self.cur_attack[Id])
            if region[2] == _Defen_:
                return
            self.scorelist[Id] += 1
            region[2] = _Defen_
            region[1] = 0
            
            
    def KeyBoardAttack(self, args):
        if not self._players[args[0]].alive:
            return
        if self.cur_attack[args[0]]:
            x = self.cur_attack[args[0]][0] + settings.Direction[args[1]][0]
            y = self.cur_attack[args[0]][1] + settings.Direction[args[1]][1]
        else:
            x = self.home[args[0]][0] + settings.Direction[args[1]][0]
            y = self.home[args[0]][1] + settings.Direction[args[1]][1]
        self._players[args[0]].set_attack(x,y)
        
    def filter_get_attack(self, id, point):
        # The point where you attack must be a neighboring point of your region
        if not point:
            return False
        flag = True
        if point in self.cur_attack.values() or point == self.home[id]:
            return False
        if point[0]<0 or point[0]>=settings.FIELD_SIZE_X or point[1]<0 or point[1]>=settings.FIELD_SIZE_Y:
            return False
        for direct in settings.Direction:
            x = point[0] + direct[0]
            y = point[1] + direct[1]
            if x>=0 and y>=0 and x<settings.FIELD_SIZE_X and y<settings.FIELD_SIZE_Y and self._world[x][y][0] == id:
                flag = True
        if flag:
            self.cur_attack[id] = copy.deepcopy(point) 
        return flag
            
    async def send_personal(self, player, *args):
        msg = json.dumps([args])
        # print(msg)
        await player.send_message(msg)    
        
    async def send_all(self, *args):
        await self.send_all_multi([args])
    
    async def send_all_multi(self, commands):
        msg = json.dumps(commands)
        # print(msg)
        for player in self._players.values():
            await player.send_message(msg)
            
    def RenderElement(self, renderlist, color, x, y):
        if color in renderlist.keys(): 
            renderlist[color].append([x,y])
        else:
            renderlist[color]=[[x,y]]