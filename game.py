from random import randint,choice
import json
import asyncio
import copy

import settings
from player import Player

class Game:

    def __init__(self):
        self._count_player = 0
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
        temp =[copy.deepcopy([0,5,'n']) for i in range(settings.FIELD_SIZE_X)]
        self._world = [copy.deepcopy(temp) for i in range(settings.FIELD_SIZE_Y)]
                
    async def new_player(self, name, ws):
        self._count_player += 1
        player_id = self._count_player
        await self.send_personal(ws, "SHAKE", name, player_id)
        player = Player(player_id, name, ws)
        self._players[player_id] = player
        return player
    
    def count_alive_players(self):
        return sum([int(p.alive) for p in self._players.values()])
        
    # The function will randomly generate one room and a color for each player 
    async def start_game(self):
        self.new_world()
        self.cur_attack = {}
        self.home = {}
        self.scorelist = {}
        colortemplist = []
        xytemplist = []
        print("STARTGAME")
        for player in self._players.values():
            x = 0
            y = 0
            color = ""
            while 1:
                x = randint(0, settings.FIELD_SIZE_X - 1)
                y = randint(0, settings.FIELD_SIZE_Y - 1)
                flag = True
                for p in xytemplist:
                    if (x - p[0])**2 + (y - p[1])**2 < 50:
                        flag = False
                if flag == True:
                    xytemplist.append([x,y])
                    break
            while 1:
                color = settings.kind_of_color[randint(0,4)]
                flag = True
                if color in colortemplist:
                    flag = False
                if flag == True:
                    colortemplist.append(color)
                    break
            player.new_game(color)
            self.cur_attack[player.get_id()] = []
            self.home[player.get_id()] = [x, y]
            self.scorelist[player.get_id()] = 0
            print("color is")
            print(color+" "+settings.GetColor(color, settings.MAX_OCCUPY))
            print("home is :")
            print([x,y])
            await self.send_all("DRAWELEMENT", [settings.GetColor(color, settings.MAX_OCCUPY), x, y])
            self._world[x][y][0] = player.get_id()
            self._world[x][y][1] = settings.OCCUPY_VALUE*settings.COLOR_LEVEL*2
            self._world[x][y][2] = 'h'
        # for line in self._world:
            # print(line)
        
    # every region will reduced 1 value each frame
    # attck region will add 5 value each frame
    async def next_frame(self):
        renderlist = {}
        # Traverse all region where players are attacking
        print("Traverse Attack")
        for player in self._players.values():
            if not player.alive:
                continue
            point = self.cur_attack[player.get_id()]
            if not point:
                self.filter_get_attack(player.get_id(), player.get_attack(self._world))
                continue
            region = self._world[point[0]][point[1]]
            if region[0] == player.get_id() :
                if region[1] > settings.MAX_OCCUPY :
                    if self.filter_get_attack(player.get_id(), player.get_attack(self._world)):
                        await self.send_all("REMOVE",[settings.GetColor(player.color, region[1]), point[0], [point[1]]])
                else:
                    region[1] = int(region[1]/settings.OCCUPY_VALUE + 1)*settings.OCCUPY_VALUE + settings.OCCUPY_VALUE
            else:
                if region[1] < 0 or region[0] == 0:
                    if region[2] == 'h':
                        await self.game_over(self._players[region[0]])
                    if region[0] != 0:
                        self.scorelist[region[0]] -= 1
                    self.scorelist[player.get_id()] += 1
                    region[0] = player.get_id()
                    region[1] = settings.OCCUPY_VALUE
                else:
                    if region[2] == 'h':
                        region[1] -= settings.OCCUPY_VALUE
                    region[1] -= settings.OCCUPY_VALUE
                    
        # Reduce all region where player has occupied values
        
        for x in range(settings.FIELD_SIZE_X):
            for y in range(settings.FIELD_SIZE_Y):
                region = self._world[x][y]
                if region[0]!=0 and region[1]>=settings.OCCUPY_VALUE*2 and region[2]!='h':
                    region[1] -= 1
                    if settings.ColorChange(region[1]):
                        color = settings.GetColor(self._players[region[0]].color,region[1])
                        if color in renderlist.keys(): 
                            renderlist[color].append([x,y])
                        else:
                            renderlist[color]=[[x,y]]
        # print("Renderlist is ")
        # print(renderlist)
        # Send changes to each client 
        for (color,points) in renderlist.items():
            await self.send_all("RENDER",[color,points])
        await self.send_all("ATTACK",list(self.cur_attack.values()))
        await self.send_all("CREATEHOME",list(self.home.values()))
        for (id,score) in self.scorelist.items():
            await self.send_all("SCORE",[id,score])
            
        
    async def game_over(self, player):
        player.alive = False
        await self.send_all("p_gameover",player.get_id())
        points = []
        for x in range(len(self._world)):
            for y in range(len(self._world[x])):
                if self._world[x][y][0] == player.get_id():
                    points.append([x,y])
                    self._world[x][y] = [0,5,'n']
        await self.send_all("RENDER",[settings.basecolor,points])
        del self.home[player.get_id()]
        del self.cur_attack[player.get_id()]
        del self.scorelist[player.get_id()]
        
    async def player_disconnected(self, player):
        player.ws = None
        if player.alive:
            render = await self.game_over(player)
            # self.apply_render(render)
        del self._players[player._id]
        del player

    
# Assist Fuction :
    def MouseAttack(self, args):
        if not self._players[args[0]].alive:
            return
        print(args)
        self._players[args[0]].set_attack(args[1],args[2])
        
    def KeyBoardAttack(self, args):
        print(args)
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
        flag = False
        print("point is:")
        print(point)
        if point in self.cur_attack.values():
            return False
        if point[0]<0 or point[0]>settings.FIELD_SIZE_X or point[1]<0 or point[1]>settings.FIELD_SIZE_Y:
            return False
        for direct in settings.Direction:
            x = point[0] + direct[0]
            y = point[1] + direct[1]
            if x>=0 and y>=0 and x<settings.FIELD_SIZE_X and y<settings.FIELD_SIZE_Y and self._world[x][y][0] == id:
                flag = True
        if flag:
            self.cur_attack[id] = point 
        print(self.cur_attack[id])
        return flag
            
    async def send_personal(self, ws, *args):
        msg = json.dumps([args])
        # print(msg)
        await ws.send_str(msg)
        return msg        
        
    async def send_all(self, *args):
        await self.send_all_multi([args])
    
    async def send_all_multi(self, commands):
        msg = json.dumps(commands)
        # print(msg)
        for player in self._players.values():
            await player._ws.send_str(msg)
                