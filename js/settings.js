const length = 25;
const height = 32;
const width = 32;
const interval = 5;
var CountOfPlayer = 0;

var CaWidth;
var CaHeight;
var playerName;
var playerId;
var GameArray;

var players = {};

function CreatePlayer(args) {
	var player = new Object();
	player.Color = args[1];
	player.Name = document.getElementById('name'+CountOfPlayer.toString());
	player.Name.innerHTML = args[2];
	player.Name.style.color = player.Color;
	player.Score = document.getElementById('score'+CountOfPlayer.toString());
	player.Score.innerHTML = '0';
	player.Score.style.color = player.Color;
	player.p = document.getElementById('player'+CountOfPlayer.toString());
	var div = document.createElement("div");
	div.className = "progress";
	var span = document.createElement("span");
	span.className = args[3];
	span.id = "span"+CountOfPlayer.toString();
	span.style.width = 0.01;
	div.appendChild(span);
	player.p.appendChild(div);
	return player;
}
