var svg = d3.select("#SVGAssemblee")
var dataset = []
var dicoNuances = {"EXG":"#d30202", "COM":"#ff1616", "FI":"#ff1616","SOC":"#f76060","RDG":"#edafaf",
"ECO":"#41992f","DIV":"#d3913b","REG":"#54422b","REM":"#af4608","MDM":"#ea681c","UDI":"#b3c5f2","LR":"#3c589e",
"DVD":"#1a3372","DLF":"#0f2763","FN":"#03194f","EXD":"#000a23"}


d3.csv('data/resultats2.csv')
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
	sore4 : d.score4
	};})
.get(function(error, rows){
	dataset = rows;
	color();
	});

function color(){
	for(i=0;i < dataset.length; i++){
		svg.select('[data-circo='+'"'+dataset[i].circo+'"'+']')
		.style("fill", dicoNuances[dataset[i].color1])
		};
	};
