var data_json;
$.getJSON("data/histogramme_partis_second_tour.json", function(json) {
    // Format de json valable : pd.to_json() avec l'option 'orient' = 'split', et les timestamps en millisecondes
    data_json = json; 

    // Prédéfinition des attributs pour 14 jeux de données au maximum (ajouter des elements a la liste si besoin)
    // couleur sous la courbe
    var backgroundColors = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)"];
    // couleur de la courbe
    var listColors = ["rgba(242,4,4,0.8)", "rgba(248,90,220,0.8)", "rgba(250,150,20,0.9)", "rgba(250,230,25,0.9)", "rgba(27,80,254,0.8)", "rgba(16,11,210,0.8)", "rgba(155,7,187,0.8)", "rgba(33,8,116,0.8)"];

    var total_candidats = [556, 414, 75, 461, 148, 480, 389, 571]
    var values = [], borderColors = [];
    var bars = [];
    var i, lenI = data_json.index.length, lenC = data_json.columns.length;
    console.log(lenI)
    for (i = 0; i < lenC; i++) {
        values[i] = [];
        var borderColors = [];

        for (j = 0; j < lenI; j++) {
            values[i].push(parseInt(data_json.data[j][i], 10) / total_candidats[j]);

            // dégradé de couleurs
            borderColors.push(listColors[j].substring(0, listColors[j].indexOf(".") + 1) + (-2*i + 9).toString() + ")");
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


    var ctx = document.getElementById("histo_partis").getContext("2d");
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
                    stacked: true,
                    ticks: {
                        callback: function(value, index, values){
                            return Math.round(value * 100) + ' %';
                        }
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        display: true,
                        stacked: false
                    },
                    gridLines: {
                        display: false,
                        lineWidth: 1
                    },
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
                    fontSize: 13,
                    text: '% des candidats présentés se maintenant au second tour'
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
                        if(i==2) { // permet de récupérer la barre la plus à droite
                            var meta = chartInstance.controller.getDatasetMeta(i);
                            meta.data.forEach(function (bar, index) {
                                var sum = 0;
                                for(var k = 0; k < values.length; k++) {
                                    sum = sum + values[k][index] * total_candidats[index];
                                }                       
                                ctx.fillText(Math.round(sum), bar._model.x + 17, bar._model.y + 7);
                            });
                        }
                    });
                }
            }
        }
    });
});
