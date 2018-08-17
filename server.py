import asyncio
import aiohttp
import json
from aiohttp import web

from game import Game
import settings

async def handle(request):
    index = open("index.html", 'rb')
    content = index.read()
    return web.Response(body=content, content_type='text/html')
	


async def wshandler(request):
    app = request.app
    ws = web.WebSocketResponse()
    game = app["game"]
    await ws.prepare(request)
    
    player = None
    while True:
        try:
            msg = await ws.receive()
        except:
            break
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            print(data)
            print("runing is "+str(game.running))
            if game.running == False :
                if data[0] == "NEWPLAYER":
                    player = await game.new_player(data[1],ws)
                    print(player)
                elif data[0] == "STARTGAME":
                    await game.start_game()
                    print("Game loop start!")
                    asyncio.ensure_future(game_loop(game))
            # elif data[0] == "join_room":
                # await game.join()
            else:
                if data[0] == "ATTAKKEYBOARD":
                    game.KeyBoardAttack(data[1])
                elif data[0] == "DEFENCEKEYBOARD":
                    game.KeyBoardDefence(data[1])
                # elif data[0] == "ATTACKMOUSE":
                    # game.MouseAttack(data[1])
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %ws.exception())
            break
        elif msg.type == aiohttp.WSMsgType.CLOSE:
            if player:
                print('player %s connection closed ' %player.get_id())
            break
            
    if player:
        await game.player_disconnected(player)
    print("Closed connection")
    return ws

async def game_loop(game):
    print("Game loop started!")
    game.running = True
    while 1:
        # try:
        await game.next_frame()
        # except Exception as e:
            # print("exception:"+str(e))
        if not game.count_alive_players():
            break
        await asyncio.sleep(1.0/settings.GAME_SPEED)
    print("Stopping game loop")
    game.running = False

app = web.Application()
app["game"] = Game()
app.router.add_route('GET', '/connect', wshandler)
app.router.add_route('GET', '/', handle)
app.router.add_static('/css/',
                       path='css',
                       name='css')
app.router.add_static('/js/',
                       path='js',
                       name='js')			   
web.run_app(app, host='127.0.0.1', port=8080)
