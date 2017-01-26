var data_json;
$.getJSON("candidats_majeurs_1d.json", function(json) {
	// Format de json valable : pd.to_json() avec l'option 'orient' = 'split', et les timestamps en millisecondes
	data_json = json; 

	// Prédéfinition des attributs pour 10 jeux de données au maximum
	// couleur sous la courbe
	var backgroundColors = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)"];
	// couleur de la courbe
	var borderColors = ["rgba(20,70,95,0.9)", "rgba(200,30,5,0.9)", "rgba(15,130,10,0.9)", "rgba(230,220,5,0.9)", "rgba(80,170,230,0.9)", "rgba(110,50,10,0.9)", "rgba(60,60,60,0.9)", "rgba(250,100,170,0.9)", "rgba(240,140,10,0.9)", "rgba(60,20,60,0.9)"];

	var values = [];
	var lines = [];
	var i, lenI = data_json.index.length, lenC = data_json.columns.length;

	for (i = 0; i < lenC; i++) { // Boucle sur les colonnes
		values[i] = [];
		for (j = 0; j < lenI; j++) { // Boucle sur les lignes
			values[i].push(data_json.data[j][i]);
		}

		lines.push({
			label : data_json.columns[i],
			backgroundColor: backgroundColors[i],
			borderColor: borderColors[i],
			data: values[i]
		});
	}

	var data = {
		labels: data_json.index,
		datasets: lines
	};

	Chart.defaults.global.elements.line.tension = .4 // coefficient de l'arrondi des courbes
	Chart.defaults.global.elements.line.borderWidth = 2

	Chart.defaults.global.elements.point.radius = 0
	Chart.defaults.global.elements.point.hoverBorderWidth = 6 // taille du point survolé
	Chart.defaults.global.elements.point.hitRadius = 14 // distance pour déclencher le tooltip

	var ctx = document.getElementById("myChart").getContext("2d");
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
					fontSize: 12,
					padding: 20
				}
			},
			responsive: true,
			//responsiveAnimationDuration: 400,
			scales: {
				xAxes: [{
					ticks: {
						autoSkip: true,
						autoSkipPadding: 30,
						fontSize: 12,
						maxRotation: 0,
						reverse: true
					}
				}],
				yAxes: [{
					position: 'right'
				}]
			},
			title: {
				display: true,
				fontSize: 16,
				text: 'Recherches sur Google'
			},
			tooltips: {
				backgroundColor: 'rgba(0,0,0,0.6)',
				cornerRadius: 0, // coefficient arrondi des bords du tooltip (0 : carré)
				mode: 'index',
				position: 'nearest'
			}
		}
	});
});

