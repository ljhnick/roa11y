let globalChartRef;

window.addEventListener('DOMContentLoaded', function () {
    
    createGraph();
    
    document.getElementById('canvas').onmousedown = function(result) {
        ourClickHandler(result);
    };
    
}, false);

function randomColor(alpha) {
    return String('rgba(' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ',' + alpha + ')');
}

function ourClickHandler(element) {
    let scaleRef,
        valueX,
        valueY;
    
    for (var scaleKey in globalChartRef.scales) {
        scaleRef = globalChartRef.scales[scaleKey];
        if (scaleRef.isHorizontal() && scaleKey == 'x-axis-1') {
            valueX = scaleRef.getValueForPixel(element.offsetX);
        } else if (scaleKey == 'y-axis-1') {
            valueY = scaleRef.getValueForPixel(element.offsetY);
        }
    }
    
    if (valueX > globalChartRef.scales['x-axis-1'].min && valueX < globalChartRef.scales['x-axis-1'].max && valueY > globalChartRef.scales['y-axis-1'].min && valueY < globalChartRef.scales['y-axis-1'].max) {
        globalChartRef.data.datasets.forEach((dataset) => {
            dataset.data.push({
                x: valueX,
                y: valueY,
                extraInfo: 'info'
            });
        });
        globalChartRef.update();
    }
}

function createGraph() {
    var config = {
        type: 'scatter',
        data: {
            datasets: [{
                label: "Dataset Made of Clicked Points",
                data: [],
                fill: false,
                showLine: true
            }]
        },
        options: {
            title: {
                display: true,
                text: "Chart.js Interactive Points"
            },
            scales: {
                xAxes: [{
                    type: "linear",
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'X-Axis'
                    },
                    ticks: {
                        min: -10,
                        suggestedMax: 5
                    }
                }, ],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Y-Axis'
                    },
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 15
                    }
                }]
            },
            responsive: true,
            maintainAspectRatio: true
        }
    };
    
    config.data.datasets.forEach(function (dataset) {
        dataset.borderColor = randomColor(0.8);
        dataset.backgroundColor = randomColor(0.7);
        dataset.pointBorderColor = randomColor(1);
        dataset.pointBackgroundColor = randomColor(1);
        dataset.pointRadius = 7;
        dataset.pointBorderWidth = 2;
        dataset.pointHoverRadius = 8;
    });
    
    var ctx = document.getElementById('canvas').getContext('2d');
    globalChartRef = new Chart(ctx, config);
}