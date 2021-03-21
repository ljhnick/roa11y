/*
	layout for the ui
*/

var container_control = $('<div class="container_control"></div>');

container_control.css("box-sizing", "border-box");
container_control.css("display", "flex");
container_control.css("flex-direction", "column");
container_control.css("align-items", "center");

container_control.css("width", "75%");
container_control.css("height", "50%");

container_control.css("overflow", "auto");



var canvas = $('<canvas id="canvas" height="100%"></canvas>');

container_control.append(canvas);

$(document.body).append(container_control);