function init(){
	GameArray = new Array();
	for(var k=0;k<width;k++){
		GameArray[k] = new Array();
		for(var j=0;j<height;j++)
			GameArray[k][j] = 0;
	}
}

function setplayer(args){
	console.log(args);
	ColorMap[args[0]] = args[1];
	NameMap[args[0]] = args[2];
	ScoreMap[args[0]] = 0;
}
function editScoreList(args){
	ScoreMap[args[0]] = args[1];
}
function gameover(Id){
	if( Id == playerId ){
		
	}
}
