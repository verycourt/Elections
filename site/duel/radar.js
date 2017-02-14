var linechart_title = "Portrait candidat"
var linechart_title = "La tendance en live"
var today = new Date();
var fname = today.getFullYear() + "-" + (((today.getMonth()+1) < 10)?"0":"") + (today.getMonth()+1) + "-" + ((today.getDate() < 10)?"0":"") + today.getDate();

$.getJSON("/duel/data/2017-02-13.json", function(json) {
	// Format de json valable : pd.to_json() avec l'option 'orient' = 'split', et les timestamps en millisecondes
	data_json = json; 

	// Prédéfinition des attributs pour 10 jeux de données au maximum (ajouter des elements a la liste si besoin)
	// couleur sous la courbe
	var backgroundColors = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)"];
	// couleur de la courbe
	var borderColors = ["rgba(20,70,95,0.9)", "rgba(200,30,5,0.9)", "rgba(15,130,10,0.9)", "rgba(230,220,5,0.9)", "rgba(80,170,230,0.9)", "rgba(110,50,10,0.9)", "rgba(60,60,60,0.9)", "rgba(250,100,170,0.9)", "rgba(240,140,10,0.9)", "rgba(60,20,60,0.9)"];

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

	console.log(max);

	for (i = 0; i < lenI; i++) {
		values[i] = [];
		for (j = 0; j < lenC; j++) {
			values[i].push(100 * data_json.data[i][j]/max[j]);
		}
		webs.push({
			label : data_json.index[i],
			backgroundColor: backgroundColors[i],
			borderColor: borderColors[i],
			data: values[i]
		});
	}

	var data = {
		labels: data_json.columns,
		datasets: webs
	};

	Chart.defaults.global.elements.line.tension = 0; // coefficient de l'arrondi des courbes
	Chart.defaults.global.elements.line.borderWidth = 4;

	Chart.defaults.global.elements.point.radius = 2;
	Chart.defaults.global.elements.point.hoverBorderWidth = 10; // taille du point survolé
	Chart.defaults.global.elements.point.hitRadius = 14; // distance pour déclencher le tooltip

	var ctx = document.getElementById("myChart").getContext("2d");
	var myLineChart = new Chart(ctx, {
		type: 'radar',
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
			responsive: true,
			//responsiveAnimationDuration: 400,
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
				titleFontSize: 13
			}
		}
	});

});