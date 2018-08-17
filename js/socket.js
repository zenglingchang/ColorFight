	function initConnect(){
		var ws_url = "ws://127.0.0.1:8080/connect";
    	ws = new WebSocket(ws_url);
		ws.onopen = openHandler;
    	ws.onmessage = messageHandler;
	}
	function sendMessage(msgArray) {
        var msg = JSON.stringify(msgArray);
        ws.send(msg);
   }
	
	function openHandler(e){
		sendMessage(["NEWPLAYER", playerName]);
	    if (1) {
	        StartGame();
	    } else {
	        nickErrorText.style.display = 'inline';
	    }
    };
    
	function messageHandler(e){
		json = JSON.parse(e.data);
		if(!(json[0] instanceof Array))
			json = [json]
		for(var i = 0; i < json.length; i++){
			var args = json[i];
			var cmd = json[i][0];
			switch(cmd){
				case("SHAKE"):
					playerId = args[1];
					break
				case("PLAYERVALUES"):
					setplayer(args[1]);
					break
				case("DRAWELEMENT"):
					drawElement(args[1]);
					break
				case("REMOVE"):
					drawElement(args[1]);
				case("CREATEHOME"):
					drawHome(args[1]);
					break
				case("DEFENCE"):
					drawDefence(args[1]);
					break
				case("RENDER"):
					render(args[1]);
					break
				case("ATTACK"):
					drawAttack(args[1]);
					break
				case("SCORE"):
					editScoreList(args[1]);
					break
				case("PGAMEOVER"):
					p_overId = args[1];
					drawgameover(p_overId);
					break

			}
		}
		
	}
