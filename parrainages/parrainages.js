var data_json;
$.getJSON("/parrainages/parrainages.json", function(json) {
    // Format de json valable : pd.to_json() avec l'option 'orient' = 'split', et les timestamps en millisecondes
    data_json = json; 

    // Prédéfinition des attributs pour 14 jeux de données au maximum (ajouter des elements a la liste si besoin)
    // couleur sous la courbe
    var backgroundColors = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)"];
    // couleur de la courbe
    var listColors = ["rgba(80,170,230,0.9)", "rgba(110,50,10,0.9)", "rgba(60,60,60,0.9)", "rgba(200,30,5,0.9)", "rgba(20,70,95,0.9)", "rgba(80,170,230,0.9)", "rgba(80,170,230,0.9)", "rgba(60,20,60,0.9)", "rgba(15,130,10,0.9)", "rgba(230,220,5,0.9)", "rgba(15,130,10,0.9)", "rgba(110,50,10,0.9)", "rgba(60,60,60,0.9)", "rgba(250,100,170,0.9)", "rgba(240,140,10,0.9)", "rgba(240,140,10,0.9)", "rgba(80,170,230,0.9)", "rgba(110,50,10,0.9)", "rgba(60,60,60,0.9)"];

    var values = [], borderColors = [];
    var bars = [];
    var i, lenI = data_json.index.length, lenC = data_json.columns.length;

    for (i = 0; i < lenC; i++) {
        values[i] = [];
        var borderColors = [];

        for (j = 0; j < lenI; j++) {
            values[i].push(parseInt(data_json.data[j][i], 10));

            // dégradé de couleurs
            borderColors.push(listColors[j].substring(0, listColors[j].indexOf(".") + 1) + (i + 4).toString() + ")");
        }

        bars.push({
            data: values[i],
            label: data_json.columns[i],
            backgroundColor: borderColors,
            borderColor: borderColors
        });
    }

    var dataBar = {
        labels: data_json.index,
        datasets: bars
    }


    var ctx = document.getElementById("chartParrainages").getContext("2d");
        var myBarChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: dataBar,
        options: {
            layout: {
                    padding: 30
                },
            legend: {
                display: false
            },
            responsive: false,
            scales: {
                xAxes: [{
                    display: true,
                    stacked: true
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        display: true
                    }
                }]
            },
            tooltips: {
                    backgroundColor: 'rgba(0,0,0,0.6)',
                    cornerRadius: 0, // coefficient arrondi des bords du tooltip (0 : carré)
                    displayColors: false,
                    enabled: true,
                    mode: 'index',
            },
            title: {
                    display: true,
                    fontSize: 16,
                    text: ''
            },
            events: false,
            hover: {
                animationDuration: 0
            },
            animation: {
                duration: 1,
                onComplete: function () {
                    var chartInstance = this.chart, ctx = chartInstance.ctx;
                    ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, 'bold', Chart.defaults.global.defaultFontFamily);
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';

                    this.data.datasets.forEach(function (dataset, i) {
                        if(i==5) { // permet de récupérer la barre la plus à droite
                            var meta = chartInstance.controller.getDatasetMeta(i);
                            meta.data.forEach(function (bar, index) {
                                var sum = 0;
                                for(var k = 0; k < values.length; k++) {
                                    sum = sum + values[k][index];
                                }                       
                                ctx.fillText(sum, bar._model.x + 17, bar._model.y + 7);
                            });
                        }
                    });
                }
            }
        }
    });
});
