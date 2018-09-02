function init(){
	CountOfPlayer = 0;
    var players = {};
	var canvas = document.getElementById('canvas');
	var cxt=canvas.getContext("2d");
	cxt.lineWidth=1.2;
	cxt.strokeStyle='black';
	for(var x = interval/2; x<canvas.width; x += length+interval ){
		for(var y= interval/2; y<canvas.height;y += length+interval ){
				cxt.moveTo(x+interval,y);
				cxt.lineTo(x+length-interval,y);
				cxt.lineTo(x+length,y+interval);
				cxt.lineTo(x+length,y+length-interval);
				cxt.lineTo(x+length-interval,y+length);
				cxt.lineTo(x+interval,y+length);
				cxt.lineTo(x,y+length-interval);
				cxt.lineTo(x,y+interval);
				cxt.lineTo(x+interval,y);
		}
	}
	cxt.stroke();
	cxt.fillStyle = "#F8F8FF";
	cxt.fill();
}

function drawAttack(Points){
	var canvas = document.getElementById('canvas');
	var cxt=canvas.getContext("2d");
	cxt.strokeStyle = 'black';
	cxt.lineWidth = 2;
	cxt.beginPath();
	for(var i=0; i<Points.length; i++){
		x=parseInt(Points[i][0])*(length+interval) + interval/2;
		y=parseInt(Points[i][1])*(length+interval) + interval/2;
		cxt.moveTo(x+interval,y+interval);
		cxt.lineTo(x+length-interval,y+length-interval);
		cxt.moveTo(x+length-interval,y+interval);
		cxt.lineTo(x+interval,y+length-interval);
	}
	cxt.closePath();
	cxt.stroke();
}

function drawHome(Points){
	var canvas = document.getElementById('canvas');
	var cxt=canvas.getContext("2d");
	cxt.strokeStyle = 'black';
	cxt.lineWidth = 2;
	cxt.beginPath();
	for(var i=0; i<Points.length; i++){
		x=parseInt(Points[i][0])*(length+interval) + interval/2;
		y=parseInt(Points[i][1])*(length+interval) + interval/2;
		cxt.moveTo(x+length/2,y+interval/2);
		cxt.lineTo(x+length-interval/2,y+length/2);
		cxt.lineTo(x+interval/2,y+length/2);
		cxt.lineTo(x+length/2,y+interval/2);
		cxt.moveTo(x+length-interval,y+length/2);
		cxt.lineTo(x+length-interval,y+length-interval/2);
		cxt.lineTo(x+interval,y+length-interval/2);
		cxt.lineTo(x+interval,y+length/2);
	}
	cxt.closePath();
	cxt.stroke();
}

function drawDefence(Points){
	var canvas = document.getElementById('canvas');
	var cxt=canvas.getContext("2d");
	cxt.strokeStyle = 'black';
	cxt.lineWidth = 2;
	cxt.beginPath();
	for(var i=0; i<Points.length; i++){
		x=parseInt(Points[i][0])*(length+interval) + interval/2;
		y=parseInt(Points[i][1])*(length+interval) + interval/2;
		cxt.moveTo(x+interval/2,y+length/2);
		cxt.lineTo(x+length-interval/2,y+length/2);
		cxt.moveTo(x+length/2-interval,y+interval);
		cxt.lineTo(x+length/2-interval,y+length-interval);
		cxt.moveTo(x+length/2,y+interval);
		cxt.lineTo(x+length/2,y+length-interval);
		cxt.moveTo(x+length/2+interval,y+interval);
		cxt.lineTo(x+length/2+interval,y+length-interval);
	}
	cxt.closePath();
	cxt.stroke();
}
function drawElement(args){
	var canvas = document.getElementById('canvas');
	var cxt=canvas.getContext("2d");
	cxt.strokeStyle = 'black';
	cxt.fillStyle = args[0];
	cxt.lineWidth=1.2;
	x=parseInt(args[1])*(length+interval) + interval/2;
	y=parseInt(args[2])*(length+interval) + interval/2;
	cxt.lineWidth=1;
	cxt.beginPath();
	cxt.moveTo(x+interval,y);
	cxt.lineTo(x+length-interval,y);
	cxt.lineTo(x+length,y+interval);
	cxt.lineTo(x+length,y+length-interval);
	cxt.lineTo(x+length-interval,y+length);
	cxt.lineTo(x+interval,y+length);
	cxt.lineTo(x,y+length-interval);
	cxt.lineTo(x,y+interval);
	cxt.lineTo(x+interval,y);
	cxt.closePath();
	cxt.stroke();
	cxt.fill();
}
function render(args){
	var canvas = document.getElementById('canvas');
	var cxt=canvas.getContext("2d");
	cxt.fillStyle = args[0];
	Points = args[1];
	cxt.lineWidth=1.2;
	cxt.strokeStyle='black';
	cxt.beginPath();
	for(var i=0; i<Points.length; i++){
		x=parseInt(Points[i][0])*(length+interval) + interval/2;
		y=parseInt(Points[i][1])*(length+interval) + interval/2;
		cxt.moveTo(x+interval,y);
		cxt.lineTo(x+length-interval,y);
		cxt.lineTo(x+length,y+interval);
		cxt.lineTo(x+length,y+length-interval);
		cxt.lineTo(x+length-interval,y+length);
		cxt.lineTo(x+interval,y+length);
		cxt.lineTo(x,y+length-interval);
		cxt.lineTo(x,y+interval);
		cxt.lineTo(x+interval,y);
	}
	cxt.closePath();
	cxt.stroke()
	cxt.fill();
}
