

function setplayer(args){
	CountOfPlayer += 1;
	players[args[0]] = CreatePlayer(args);
	console.log(players);
}

function editScoreList(args){
	players[args[0]].Score.innerHTML = args[1];
	document.getElementById('span'+args[0]).style.width = parseInt(args[1])/1024;
}
function gameover(Id){
	if( Id == playerId ){
		
	}
}
