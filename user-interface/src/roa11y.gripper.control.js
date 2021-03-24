// let globalChartRef;
var ROA11Y = ROA11Y || {};

class InteractiveGraph {
    constructor (canvas, canvas_ref, data_template) {
        this._dataInitial = data_template;
        this._canvas = canvas;
        this._canvasRef = canvas_ref;

        this._generateConfig();
        this._updateGraphStyle();
        this._init();
        this._generateReference();
    }

    _generateConfig() {
        var config = {
            type: 'scatter',
            data: {
                datasets: [{
                    data: this._dataInitial,
                    fill: true,
                    showLine: true,
                    pointBackgroundColor: 'rgba(52, 40, 189, 0.8)',
                    pointRadius: 4,
                    borderColor: 'rgba(52, 40, 189, 0.4)',
                    backgroundColor: 'rgba(52, 40, 189, 0.4)'
                }]
            },
            options: {
                title: {
                    display: true,
                    text: "Control input"
                },
                scales: {
                    xAxes: [{
                        type: "linear",
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time (s)'
                            },
                        ticks: {
                            min: 0,
                            suggestedMax: 5
                            },
                        gridLines: {
                            drawTicks: false
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'u'
                        },
                        ticks: {
                            min: -1,
                            max: 1,
                            precision: 0
                        },
                        gridLines: {
                            drawTicks: true
                        }
                    }]
                },
                responsive: true,
                maintainAspectRatio: true,
                legend: {
                    display: false
                }
            }
        };

        this._config = config;
    }

    _generateConfigRef() {
        var config = {
            type: 'line',
            data: {
                datasets: [{
                    data: [{x:0, y:0}], 
                    tension: 0,
                    fill: false,
                    pointBackgroundColor: 'rgba(219, 26, 71, 0.8)',
                    pointRadius: 2,
                    borderColor: 'rgba(219, 26, 71, 0.8)',
                }]
            },
            options: {
                title: {
                    display: true,
                    text: "Reference"
                }, 
                scales: {
                    xAxes: [{
                        type: "linear",
                        display: true,
                        scaleLabel: {
                            display: true,
                            // labelString: 'Time (s)'
                        },
                        ticks: {
                            beginAtZero: true,
                            suggestedMax: 5
                        }
                    }, ],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Distance'
                        },
                        ticks: {
                            suggestedMin: -1,
                            suggestedMax: 5,
                            precision: 0
                        },
                        gridLines: {
                            drawTicks: true
                        }
                    }, ]
                },
                responsive: true,
                legend: {
                    display: false
                }
            }
        };

        this._configRef = config;
    }

    _updateGraphStyle() {
        var dataset_u = this._config.data.datasets[0];
        var dataset_d = this._config.data.datasets[1];
        dataset_u.steppedLine = true;
    }

    _generateReference() {
        var ctx = this._canvasRef[0].getContext('2d');
        this._generateConfigRef();
        this.chartRef = new Chart(ctx, this._configRef);
        this.updateRefData();
    }

    _init() {
        var ctx = this._canvas[0].getContext('2d');
        this.chart = new Chart(ctx, this._config);
    }

    addHorizontalRange() {
        var previousX = this.chart.options.scales.xAxes[0].ticks.suggestedMax;
        var scale_value = (1+previousX)/previousX;

        this.chart.data.datasets[0].data.forEach((data) => {
            data.x *= scale_value;
        });

        this.chart.options.scales.xAxes[0].ticks.suggestedMax += 1
        this.chart.update();
        this.updateRefData();
    }

    subtractHorizontalRange() {
        var previousX = this.chart.options.scales.xAxes[0].ticks.suggestedMax;
        var scale_value = (previousX-1)/previousX;

        this.chart.data.datasets[0].data.forEach((data) => {
            data.x *= scale_value;
        });

        this.chart.options.scales.xAxes[0].ticks.suggestedMax -= 1
        this.chart.update();
        this.updateRefData();
    }

    updateAll() {
        this.chart.update();
        this.updateRefData();
    }

    updateRefData() {
        var data = this.chart.data.datasets[0].data;
        // var dataRef = this.chartRef.data.datasets[0].data;
        this._dataRef = [{x:0, y:0}];
        for (var i = 0; i < data.length-1; i++) {
            var x = data[i+1].x;
            var y = (data[i+1].x-data[i].x)*data[i].y*2 + this._dataRef[i].y;
            this._dataRef.push({x:x, y:y});
        }
        this.chartRef.data.datasets[0].data = this._dataRef;

        this.chartRef.options.scales.xAxes[0].ticks.suggestedMax = this.chart.options.scales.xAxes[0].ticks.suggestedMax;

        this.chartRef.update();
    }

    selectData(event) {
        var element = this.chart.getElementAtEvent(event)[0];
        if (element != undefined) {
            this.modifyingDataIndex = element['_index'];
            this.modifyingDataIdX = element['_xScale'].id;
            this.modifyingDataIdY = element['_yScale'].id;
            this.modifyDataFlag = true;
        }
        // console.log(element);
    }

    modifyData(event) {
        // console.log(event.clientX);
        var valueX = this.chart.scales[this.modifyingDataIdX].getValueForPixel(event.offsetX);
        var valueY = this.chart.scales[this.modifyingDataIdY].getValueForPixel(event.offsetY);
        valueY = Math.max(Math.min(1, valueY), -1);
        valueX = Math.max(valueX, 0);
        this.chart.data.datasets[0].data[this.modifyingDataIndex].x = valueX;
        this.chart.data.datasets[0].data[this.modifyingDataIndex].y = valueY;
        this.chart.update();
        this.updateRefData();
    }



}

// window.addEventListener('DOMContentLoaded', function () {   

//     document.getElementById('canvas').onmousedown = function(result) {
//         ourClickHandler(result);
//     }; 

// }, false);

function ourClickHandler(element) {
    let scaleRef,
        valueX,
        valueY;
    
    for (var scaleKey in ROA11Y.designControl.chart.scales) {
        scaleRef = ROA11Y.designControl.chart.scales[scaleKey];
        if (scaleRef.isHorizontal() && scaleKey == 'x-axis-1') {
            valueX = scaleRef.getValueForPixel(element.offsetX);
        } else if (scaleKey == 'y-axis-1') {
            valueY = scaleRef.getValueForPixel(element.offsetY);
        }
    }
    
    if (valueX > ROA11Y.designControl.chart.scales['x-axis-1'].min && valueX < ROA11Y.designControl.chart.scales['x-axis-1'].max && valueY > ROA11Y.designControl.chart.scales['y-axis-1'].min && valueY < ROA11Y.designControl.chart.scales['y-axis-1'].max) {
        // globalChartRef.data.datasets.forEach((dataset) => {
        //     dataset.data.push({
        //         x: valueX,
        //         y: valueY,
        //         extraInfo: 'info'
        //     });
        // });
        ROA11Y.designControl.chart.data.datasets[0].data.push({
            x: valueX,
            y: valueY,
        });
        ROA11Y.designControl.chart.update();
        ROA11Y.designControl.updateRefData();
    }
}

canvas.on('click', function(event) {
    event.preventDefault();
    if ($('#addPoint').prop('checked')) {
        ourClickHandler(event);
    }
});

canvas.on('mousedown', function(event) {
    event.preventDefault();
    /* Act on the event */
    if (!$('#addPoint').prop('checked')) {
        ROA11Y.designControl.selectData(event);
    }
});

canvas.on('mousemove', function(event) {
    event.preventDefault();
    /* Act on the event */
    if (ROA11Y.designControl.modifyDataFlag) {
        ROA11Y.designControl.modifyData(event);
    }

});

canvas.on('mouseup', function(event) {
    if (!$('#addPoint').prop('checked')) {
        ROA11Y.designControl.modifyDataFlag = false;
    }
});

ROA11Y.templateData = $.getJSON('assets/template.json');
// ROA11Y._templateData = templateData.responseJSON;
var data_template = [{x: 0, y: 1}, {x: 0.2, y: 0.5}, {x: 0.4, y:-1}];
ROA11Y.designControl = new InteractiveGraph(canvas, canvas_dist, data_template);


    
//     config.data.datasets.forEach(function (dataset) {
//         // dataset.borderColor = randomColor(0.8);
//         // dataset.backgroundColor = randomColor(0.7);
//         // dataset.pointBorderColor = randomColor(1);
//         // dataset.pointBackgroundColor = randomColor(1);
//         dataset.pointRadius = 7;
//         dataset.pointBorderWidth = 2;
//         dataset.pointHoverRadius = 8;
//         dataset.steppedLine = true;
//     });
    



