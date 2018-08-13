const length = 25;
const height = 32;
const width = 32;
const interval = 5;
var CaWidth;
var CaHeight;
var playerName;
var playerId;
var MyColor;
var GameArray;

window.onload = function () {
    var btn = document.getElementById('startButton'),
        nickErrorText = document.querySelector('#startMenu .input-error');
    btn.onclick = function () {
		initConnect()
    	playerName=document.getElementById('playerNameInput').value;

    };
};

function StartGame(){
	var wrap=document.getElementById('startMenuWrapper');
	wrap.parentNode.removeChild(wrap);
	document.getElementById("GameWrap").style.visibility="visible";
	var btn = document.getElementById('GameButton');
	btn.onclick = function(){
		sendMessage(["STARTGAME",playerName]);
	}
	var canvas = document.createElement('canvas');
	canvas.width = width*(length + interval);
	canvas.height = height*(length + interval);
	canvas.id='canvas';
	var container=document.getElementById('container');
	container.style.backgroundColor="rgb(253,255,255)";
	container.appendChild(canvas);	
	HRatio = height/(canvas.getBoundingClientRect().bottom - canvas.getBoundingClientRect().top);
	WRatio = width/(canvas.getBoundingClientRect().right - canvas.getBoundingClientRect().left);
	console.log([WRatio,HRatio]);
	canvas.addEventListener('click', function(e) {
		x = (e.clientX - canvas.getBoundingClientRect().left)*WRatio
		y = (e.clientY - canvas.getBoundingClientRect().top)*HRatio;
		sendMessage(["ATTACKMOUSE", [playerId, parseInt(x), parseInt(y)]]);
   })
	init();
	document.onkeydown=function(event){
	var e = event || window.event || arguments.callee.caller.arguments[0];
	if(e && e.keyCode>=37 && e.keyCode <= 40){ //left up right down 
		sendMessage(["ATTAKKEYBOARD", [playerId, e.keyCode-37]]);
	}
}; 
}
