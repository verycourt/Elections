var fname = "4_yt_reaction_rate.json";

$.getJSON("/metrics/data/" + fname, function(json) {
    var linechart_title = "Réactions aux vidéos YouTube (rapport pouces bleus et pouces rouges cumulés sur nombre total de vues)"
    var chart_id = "m4"
    // Format de json valable : pd.to_json() avec l'option 'orient' = 'split', et les timestamps en millisecondes
    var data_json = json; 

    // Prédéfinition des attributs pour 10 jeux de données au maximum (ajouter des elements a la liste si besoin)
    // couleur sous la courbe
    var backgroundColors = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)"];
    
    // couleur de la courbe
    // var borderColors = ["rgba(20,70,95,0.9)", "rgba(200,30,5,0.9)", "rgba(15,130,10,0.9)", "rgba(230,220,5,0.9)", "rgba(80,170,230,0.9)", "rgba(110,50,10,0.9)", "rgba(60,60,60,0.9)", "rgba(250,100,170,0.9)", "rgba(240,140,10,0.9)", "rgba(60,20,60,0.9)"];
    var borderColors = ["rgba(30,40,180,0.9)", "rgba(250,100,170,0.9)", "rgba(20,70,95,0.9)", "rgba(110,50,10,0.9)", "rgba(225,5,5,0.9)"]
    
    var lines = [];
    var lenI = data_json.index.length;

    for (var i = 0; i < lenI; i++) { // Boucle sur les lignes
        lines.push({
            label : data_json.index[i],
            backgroundColor: backgroundColors[i],
            borderColor: borderColors[i],
            data: data_json.data[i]
        });
    }

    var data = {
        labels: data_json.columns,
        datasets: lines
    };

    Chart.defaults.global.elements.line.tension = 0; // coefficient de l'arrondi des courbes
    Chart.defaults.global.elements.line.borderWidth = 2;

    Chart.defaults.global.elements.point.radius = 2;
    Chart.defaults.global.elements.point.hoverBorderWidth = 10; // taille du point survolé
    Chart.defaults.global.elements.point.hitRadius = 14; // distance pour déclencher le tooltip

    var ctx = document.getElementById(chart_id).getContext("2d");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            layout: {
                padding: 40
            },
            legend: {
                labels: {
                    boxWidth: 15,
                    fontSize: 14,
                    padding: 15
                }
            },
            responsive: false,
            //responsiveAnimationDuration: 400,
            scales: {
                xAxes: [{
                    ticks: {
                        autoSkip: true,
                        autoSkipPadding: 30,
                        fontSize: 12,
                        maxRotation: 0,
                    },
                    type: 'time',
                    time: {
                        displayFormats: {
                            day: 'DD MMMM'
                        },
                        tooltipFormat: 'DD MMMM'
                    }
                }],
                yAxes: [{
                    position: 'right',
                    ticks: {
                        fontSize: 12,
                        callback: function(value, index, values) {
                            return value + '%';
                        }
                    }
                }]
            },
            title: {
                display: true,
                fontSize: 16,
                text: linechart_title
            },
            tooltips: {
                backgroundColor: 'rgba(0,0,0,0.6)',
                caretSize: 8,
                cornerRadius: 0, // coefficient arrondi des bords du tooltip (0 : carré)
                mode: 'index',
                position: 'nearest',
                bodyFontSize: 13,
                titleFontSize: 13,
                callbacks: { // formate les valeurs en format francais (local)
                    label: function(tooltipItems, data) {
                        return data.datasets[tooltipItems.datasetIndex].label +': ' + data_json.data[tooltipItems.datasetIndex][tooltipItems.index].toLocaleString();
                    }
                }
            }
        }
    });
});