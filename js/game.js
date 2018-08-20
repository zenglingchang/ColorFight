function init(){
	GameArray = new Array();
	for(var k=0;k<width;k++){
		GameArray[k] = new Array();
		for(var j=0;j<height;j++)
			GameArray[k][j] = 0;
	}
}

function setplayer(args){
	CountOfPlayer += 1;
	players[args[0]] = CreatePlayer(args);
	console.log(players);
}

function editScoreList(args){
	players[args[0]].Score.innerHTML = args[1];
}
function gameover(Id){
	if( Id == playerId ){
		
	}
}
