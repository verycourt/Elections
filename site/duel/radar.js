var linechart_title = "Veille réseaux sociaux"
var today = new Date();
var fname = today.getFullYear() + "-" + (((today.getMonth()+1) < 10)?"0":"") + (today.getMonth()+1) + "-" + ((today.getDate() < 10)?"0":"") + today.getDate();
console.log(fname);

$.getJSON("/duel/data/" + fname + ".json", function(json) {
    // Format de json valable : pd.to_json() avec l'option 'orient' = 'split', et les timestamps en millisecondes
    data_json = json; 

    // Prédéfinition des attributs pour 10 jeux de données au maximum (ajouter des elements a la liste si besoin)
    // couleur sous la courbe
    var backgroundColors = ["rgba(80,170,230,0.1)", "rgba(50,50,50,0.1)", "rgba(240,140,10,0.1)", "rgba(230,220,5,0.1)",
    "rgba(60,20,60,0.1)", "rgba(30,40,180,0.1)", "rgba(250,100,170,0.1)", "rgba(15,130,10,0.1)",
    "rgba(20,70,95,0.1)", "rgba(110,50,10,0.1)", "rgba(225,5,5,0.1)", "rgba(160,10,10,0.1)"];
    // couleur de la courbe
    var borderColors = ["rgba(80,170,230,0.9)", "rgba(50,50,50,0.9)", "rgba(240,140,10,0.9)", "rgba(230,220,5,0.9)",
    "rgba(60,20,60,0.9)", "rgba(30,40,180,0.9)", "rgba(250,100,170,0.9)", "rgba(15,130,10,0.9)",
    "rgba(20,70,95,0.9)", "rgba(110,50,10,0.9)", "rgba(225,5,5,0.9)", "rgba(160,10,10,0.9)"];

    var values = [];
    var webs = [], temp = [], max = [];
    var i, lenI = data_json.index.length, lenC = data_json.columns.length;
    var maxi = 0;

    for (i = 0; i < lenC; i++) { // Boucle sur les colonnes
        maxi = 0;
        for (j = 0; j < lenI; j++) { // Boucle sur les lignes
            if (data_json.data[j][i] > maxi) {
                maxi = data_json.data[j][i];
            }
        }
        max.push(maxi); // valeur maximum pour chaque indicateur
    }

    for (i = 0; i < lenI; i++) {
        values[i] = [];
        for (j = 0; j < lenC; j++) {
            values[i].push(Math.round(100 * data_json.data[i][j]/max[j]));
        }
        webs.push({
            label : data_json.index[i],
            backgroundColor: backgroundColors[i],
            borderColor: borderColors[i],
            data: values[i]
        });
    }

    var data = {
        labels: ['Followers Twitter', 'Total tweets', 'Abonnés YouTube', 'Vues en moyenne',
    '% de "j\'aime" des vidéos', '% de "je n\'aime pas" des vidéos', '"Likes" Facebook', 'En parlent sur Facebook'],
        datasets: webs
    };

    Chart.defaults.global.elements.line.borderWidth = 4;
    Chart.defaults.global.elements.point.radius = 0;
    Chart.defaults.global.elements.point.hitRadius = 14; // distance pour déclencher le tooltip

    var ctx = document.getElementById("myChart").getContext("2d");
    var myLineChart = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: { 
            layout: {
                padding: 20
            },
            legend: {
                labels: {
                    boxWidth: 15,
                    fontSize: 12,
                    padding: 15
                },
                position: 'right'
            },
            responsive: false,
            //responsiveAnimationDuration: 400,
            scale: {
                pointLabels: {
                    fontSize: 12,
                },
                ticks: {
                    display: false
                }
            },
            startAngle: 22.5, // rotation du graph en degrés
            title: {
                display: true,
                fontSize: 18,
                text: linechart_title
            },
            tooltips: {
                bodyFontSize: 13,
                backgroundColor: 'rgba(0,0,0,0.6)',
                caretSize: 8,
                cornerRadius: 0, // coefficient arrondi des bords du tooltip (0 : carré)
                displayColors: false,
                mode: 'index',
                position: 'nearest',
                titleFontSize: 13,
                callbacks: {
                    label: function(tooltipItems, data) {
                        return data.datasets[tooltipItems.datasetIndex].label +': ' + data_json.data[tooltipItems.datasetIndex][tooltipItems.index].toLocaleString();
                    }
                }
            }
        }
    });

});