var svg2 = d3.select("svg#svg4195")
var dataset2 = []
var dicoNuances2 = {"EXG":"#d30202", "COM":"#ff1616", "FI":"#ff1616","SOC":"#f76060","RDG":"#edafaf",
"ECO":"#41992f","DIV":"#d3913b","REG":"#54422b","REM":"#ffbf00","MDM":"#ed9302","UDI":"#536cad","LR":"#3c589e",
"DVD":"#1a3372","DLF":"#7928b7","FN":"#03194f","EXD":"#000a23","DVG":"#c66b9a"}

d3.csv('data/resultats1.csv')
.row(function(d, i){
	return {
	circo : d.circo,
	nom : d["nom circo"],
	color1 : d.color1,
	candidat1 : d.candidat1,
	score1 : d.score1,
	candidat2 : d.candidat2,
	score2 : d.score2,
	candidat3 : d.candidat3,
	score3 : d.score3,
	candidat4 : d.candidat4,
	color2 : d.color2,
	color3 : d.color3,
	score4 : d.score4
	};
})
.get(function(error, rows){
	dataset2 = rows;
	colorMap();
	});

d3.csv('data/resultatsEtr.csv')
.row(function(d, i){
	return {
	circo : d.circo,
	nom : d["nom circo"],
	color1 : d.color1,
	candidat1 : d.candidat1,
	score1 : d.score1,
	candidat2 : d.candidat2,
	score2 : d.score2,
	candidat3 : d.candidat3,
	score3 : d.score3,
	candidat4 : d.candidat4,
	color2 : d.color2,
	color3 : d.color3,
	score4 : d.score4
	};
})
.get(function(error, rows){
	dataset2 = rows;
	colorMap();
	});



function colorMap(){
	for(i=0;i < dataset2.length; i++){
		if(dataset2[i].color1 == "LR" || dataset2[i].color1 == "UDI" ){
			svg2.select('[id='+'"'+dataset2[i].circo+'"'+']').style("fill", dicoNuances2[dataset2[i].color1])
		}
		else{
			if(dataset2[i].color2 == "LR" || dataset2[i].color2 == "UDI"){
			svg2.select('[id='+'"'+dataset2[i].circo+'"'+']').style("fill", dicoNuances2[dataset2[i].color2])
			}
			else{
				if(dataset2[i].color3 == "LR" || dataset2[i].color3 == "UDI"){
				svg2.select('[id='+'"'+dataset2[i].circo+'"'+']').style("fill", dicoNuances2[dataset2[i].color3])
			}

			}
		}
	};
};
