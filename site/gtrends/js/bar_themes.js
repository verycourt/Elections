var data_json;
$.getJSON("./data/themes_7j.json", function(json) {
	// Format de json valable : pd.to_json() avec l'option 'orient' = 'split', et les timestamps en millisecondes
	data_json = json; 

	// Prédéfinition des attributs pour 10 jeux de données au maximum (ajouter des elements a la liste si besoin)
	// couleur sous la courbe
	var backgroundColors = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)"];
	// couleur de la courbe
	var borderColors = ["rgba(20,70,95,0.9)", "rgba(200,30,5,0.9)", "rgba(15,130,10,0.9)", "rgba(230,220,5,0.9)", "rgba(80,170,230,0.9)", "rgba(110,50,10,0.9)", "rgba(60,60,60,0.9)", "rgba(250,100,170,0.9)", "rgba(240,140,10,0.9)", "rgba(60,20,60,0.9)"];

	var values = [];
	var lines = [], bars = [], moyennes = [];
	var i, lenI = data_json.index.length, lenC = data_json.columns.length;


	function mean(numbers) {
		// mean of [3, 5, 4, 4, 1, 1, 2, 3] is 2.875
		var total = 0,
			i;
		for (i = 0; i < numbers.length; i += 1) {
			total += numbers[i];
		}
		return total / numbers.length;
	}

	for (i = 0; i < lenC; i++) { // Boucle sur les colonnes
		values[i] = [];
		for (j = 0; j < lenI; j++) { // Boucle sur les lignes
			values[i].push(parseInt(data_json.data[j][i], 10));
		}

		moyennes.push(Math.round(mean(values[i]))); // valeur moyenne arrondie

	}

	bars.push({
		data: moyennes,
		backgroundColor: borderColors.slice(0, lenC),
		borderColor: borderColors.slice(0, lenC)
	});


	var dataBar = {
		labels: data_json.columns,
		datasets: bars
	}


	var ctx2 = document.getElementById("myBarChart").getContext("2d");
	var myBarChart = new Chart(ctx2, {
	type: 'bar',
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
			}],
			yAxes: [{
				ticks: {
					beginAtZero: true,
					display: false
				}
			}]
		},
		tooltips: {
				backgroundColor: 'rgba(0,0,0,0.6)',
				cornerRadius: 0, // coefficient arrondi des bords du tooltip (0 : carré)
				mode: 'index',
		},
		title: {
				display: true,
				fontSize: 16,
				text: 'Moyennes entre le 21 et le 27 janvier'
		}
	}
});
});

