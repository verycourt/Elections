var data_json;
$.getJSON("/parrainages/parrainages.json", function(json) {
	// Format de json valable : pd.to_json() avec l'option 'orient' = 'split', et les timestamps en millisecondes
	data_json = json; 

	// Prédéfinition des attributs pour 10 jeux de données au maximum (ajouter des elements a la liste si besoin)
	// couleur sous la courbe
	var backgroundColors = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)"];
	// couleur de la courbe
	var listColors = ["rgba(20,70,95,0.9)", "rgba(200,30,5,0.9)", "rgba(15,130,10,0.9)", "rgba(230,220,5,0.9)", "rgba(80,170,230,0.9)", "rgba(110,50,10,0.9)", "rgba(60,60,60,0.9)", "rgba(250,100,170,0.9)", "rgba(240,140,10,0.9)", "rgba(60,20,60,0.9)"];

	var values = [], series = [], borderColors = [];
	var bars = [];
	var i, lenI = data_json.index.length, lenC = data_json.columns.length;

	for (i = 0; i < lenC; i++) {
		values[i] = [];
		var borderColors = [];
		series.push(data_json.columns[i]);
		console.log(borderColors);
		for (j = 0; j < lenI; j++) {
			values[i].push(parseInt(data_json.data[j][i], 10));

			// dégradé de couleurs
			borderColors.push(listColors[j].substring(0, listColors[j].indexOf(".") + 1) + (i + 5).toString() + ")");
		}

		bars.push({
			data: values[i],
			label: series[i],
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
				padding: 5
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
				mode: 'index',
		},
		title: {
				display: true,
				fontSize: 16,
				text: 'Parrainages obtenus'
		}
	}
});
});

