var data_json;
$.getJSON('/gtrends/data/candidats_majeurs_4h.json', function(json) {
  // Format de json valable : pd.to_json() avec l'option 'orient' = 'split', et les timestamps en millisecondes
  data_json = json; 

  var i, lenI = data_json.index.length, lenC = data_json.columns.length;

	var values = [];
	for (i = 0; i < lenC; i++) { // looping on the columns
		values[i] = [];
	    for (j = 0; j < lenI; j++) { // looping on the values
	        values[i].push(data_json.data[j][i]);
	    }
	}
	console.log(values);
	// TODO: adapter dynamiquement le nombre de datasets par rapport au contenu du json
	var data = {
	labels: data_json.index,
	datasets: [
	    {
	        label: data_json.columns[0],
	        backgroundColor: "rgba(0,0,0,0)",
	        borderColor: "rgba(0,50,220,0.8)",
	        highlightFill: "rgba(0,50,220,0.75)",
	        highlightStroke: "rgba(0,50,220,1)",
	        data: values[0]
	    },
	    {
	        label: data_json.columns[1],
	        backgroundColor: "rgba(0,0,0,0)",
	        borderColor: "rgba(0,200,0,0.8)",
	        highlightFill: "rgba(0,200,0,0.75)",
	        highlightStroke: "rgba(0,200,0,1)",
	        data: values[1]
	    },
	    {
	        label: data_json.columns[2],
	        backgroundColor: "rgba(0,0,0,0)",
	        borderColor: "rgba(204,204,0,0.8)",
	        highlightFill: "rgba(204,204,0,0.75)",
	        highlightStroke: "rgba(204,204,0,1)",
	        data: values[2]
	    },
	    {
	        label: data_json.columns[3],
	        backgroundColor: "rgba(0,0,0,0)",
	        borderColor: "rgba(151,0,0,0.8)",
	        highlightFill: "rgba(151,0,0,0.75)",
	        highlightStroke: "rgba(151,0,0,1)",
	        data: values[3]
	    },
	    {
	        label: data_json.columns[4],
	        backgroundColor: "rgba(0,0,0,0)",
	        borderColor: "rgba(51,0,51,0.8)",
	        highlightFill: "rgba(51,0,51,0.75)",
	        highlightStroke: "rgba(51,0,51,1)",
	        data: values[4]
	    }
	]
	};

	var ctx = document.getElementById("elem1").getContext("2d");
	var myLineChart = new Chart(ctx, {
	    type: 'line',
	    data: data,
	    options: {
	    	layout: {
	    		padding: 20
	    	},
	        title: {
	            display: true,
	            text: 'Recherches Google : les 4 dernières heures.',
	            fontSize: 16
	        },
	        scales: {
	            xAxes: [{
	                type: 'time',
	                time: {
	                    displayFormats: {
	                        quarter: 'MMM YYYY'
	                    }
	                }
	            }]
	        },
	        legend: {
	        	labels: {
	        		padding: 15,
	        		boxWidth: 20
	        	}
	        },
	        tooltips: {
	        	mode: 'index',
	        	callbacks: {
	        		title: function(tooltipItem, data) {
	        			return
	        		}
	        	}
	        },
	        responsive: true
	    }
	});
});

