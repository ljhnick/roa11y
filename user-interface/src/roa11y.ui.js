/*
	layout for the ui
*/

var ROA11Y = ROA11Y || {};

// panel
						
var panel = $('<div></div>');
panel.css('width', ROA11Y.PANELWIDTH + 'px');
panel.css('height', '100%');
panel.css('color', '#000000');
panel.css('background-color', 'rgba(192, 192, 192, 0.50)');
panel.css('top', '0px');
panel.css('position', 'absolute');
panel.css('font-family', 'Helvetica');
panel.css('overflow', 'auto');
panel.css('padding', 10 + 'px');
panel.css('overflow', 'hidden');

panel.load(ROA11Y.TABLEPANEL, function(e) {
	// add button
	//
	//
	// $('#btnRealTest').button();
	// $('#btnRealTest').css('padding', '.0em .6em');

    $('#btnRealTest').click(function (e) {
    	e.preventDefault();
	    var msg = ROA11Y.designControl.chart.data;
	    // msg.datasets[0].data.push({x: designControl.chart.options.scales.xAxes[0].ticks.suggestedMax, y: 0});
	    msg = JSON.stringify(ROA11Y.designControl.chart.data.datasets[0].data);
	    msg = 'test|' + msg;

	    xmlhttp.open('POST', ip_port, true);
	    xmlhttp.send(msg);
        e.preventDefault();
    });

    $('#btnAddTime').click(function (e) {
    	e.preventDefault();
    	ROA11Y.designControl.addHorizontalRange();
    });

    $('#btnSubtractTime').click(function (e) {
    	e.preventDefault();
    	ROA11Y.designControl.subtractHorizontalRange();
    });

    $('#btnSave').click(function (e) {
    	e.preventDefault();
    	var msg = JSON.stringify(ROA11Y.designControl.chart.data.datasets[0].data);
    	msg = 'save|' + msg;

    	xmlhttp.open('POST', ip_port, true);
	    xmlhttp.send(msg);
        e.preventDefault();
    });

    $('#btnRead').click(function (e) {
    	e.preventDefault();
    	var msg = JSON.stringify(ROA11Y.designControl.chart.data.datasets[0].data);
    	msg = 'read|' + msg;

    	xmlhttp.open('POST', ip_port, true);
	    xmlhttp.send(msg);

	    // console.log(xmlhttp.responseText);

	    xmlhttp.onreadystatechange = function () {
		    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
		        console.log('server response: ' + xmlhttp.responseText);
			    var readData = JSON.parse(xmlhttp.responseText);
			    // console.log(readData);
			    ROA11Y.designControl.chart.data.datasets[0].data = JSON.parse(readData);
			    ROA11Y.designControl.updateAll();		        
		    }
		}
        e.preventDefault();
    });

    ROA11Y._listTemplate = $('#listTemplate');
    ROA11Y._listTemplate.css('background-color', 'rgba(255, 255, 255, 0.5)');
    ROA11Y._listTemplate.css('padding', 0);
    ROA11Y._listTemplate.load(ROA11Y.TEMPLATELIST, function(e) {

    	var dataJSON = ROA11Y.templateData.responseJSON;
		$('#rotation').on('click', function(event) {
			event.preventDefault();
			/* Act on the event */
			var data = dataJSON.rotation.data;
			ROA11Y.designControl.chart.data.datasets[0].data = data;
			ROA11Y.designControl.chart.update();
			ROA11Y.designControl.updateRefData();
		});

		$('#periodic').on('click', function(event) {
			event.preventDefault();
			/* Act on the event */
			var data = dataJSON.periodic.data;
			ROA11Y.designControl.chart.data.datasets[0].data = data;
			ROA11Y.designControl.chart.update();
			ROA11Y.designControl.updateRefData();
		});

		$('#oneway').on('click', function(event) {
			event.preventDefault();
			/* Act on the event */
			var data = dataJSON.oneway.data;
			ROA11Y.designControl.chart.data.datasets[0].data = data;
			ROA11Y.designControl.chart.update();
			ROA11Y.designControl.updateRefData();
		});

		$('#twoway').on('click', function(event) {
			event.preventDefault();
			/* Act on the event */
			var data = dataJSON.twoway.data;
			ROA11Y.designControl.chart.data.datasets[0].data = data;
			ROA11Y.designControl.chart.update();
			ROA11Y.designControl.updateRefData();
		});
    });

})

// panel.load(ROA11Y.TABLEPANEL);
// $('#btnRealTest').button();

// $('#btnSave').button();

// var btn_test = $('<button>Real test</button>');
// panel.append(btn_test);

// var btn_save = $('<button>save data</button>');
// panel.append(btn_save);

// var btn_addtime = $('<button>+</button>');
// panel.append(btn_addtime);

$(document.body).append(panel);


// interactive graph

var container_control = $('<div class="container_control"></div>');

container_control.css("box-sizing", "border-box");
container_control.css("display", "flex");
container_control.css("flex-direction", "column");
container_control.css("align-items", "center");

container_control.css("width", "1200px");
container_control.css("height", "100%");

container_control.css("overflow", "auto");

container_control.css('left', ROA11Y.PANELWIDTH +'px');
container_control.css('position', 'absolute');


// two canvas
var canvas_dist = $('<canvas id="canvas_dist" height="100%"></canvas>');
container_control.append(canvas_dist);

var canvas = $('<canvas id="canvas" height="100%"></canvas>');
container_control.append(canvas);


$(document.body).append(container_control);


// btn_test.on("click", function (event) {
//     event.preventDefault();
//     var msg = designControl.chart.data;
//     // msg.datasets[0].data.push({x: designControl.chart.options.scales.xAxes[0].ticks.suggestedMax, y: 0});
//     msg = JSON.stringify(designControl.chart.data.datasets[0].data);

//     xmlhttp.open('POST', ip_port, true);
//     xmlhttp.send(msg);

// });


// btn_addtime.on("click", function (event) {
//     event.preventDefault();
//     designControl.addHorizontalRange();

// });		




