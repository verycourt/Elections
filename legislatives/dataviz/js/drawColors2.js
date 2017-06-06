var svg2 = d3.select("svg#second")
var dataset2 = []
var dicoNuances = {"EXG":"#d30202", "COM":"#ff1616", "FI":"#ff1616","SOC":"#f76060","RDG":"#edafaf",
"ECO":"#41992f","DIV":"#d3913b","REG":"#54422b","REM":"#ffbf00","MDM":" #cca300","UDI":"#536cad","LR":"#3c589e",
"DVD":"#1a3372","DLF":"#7928b7","FN":"#03194f","EXD":"#000a23","DVG":"#c66b9a"}

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
	};
})
.get(function(error, rows){
	dataset2 = rows;
	colorMap();
	});

function colorMap(){
	for(i=0;i < dataset2.length; i++){
		svg2.select('[id='+'"'+dataset2[i].circo+'"'+']')
		.style("fill", dicoNuances[dataset2[i].color1])
		.select("title").text(function(){
			return dataset2[i].nom +'\n' + dataset2[i].candidat1 + " : " + dataset2[i].score1 * 100 +"%" + "(Vainqueur)" + '\n' 
		+ dataset2[i].candidat2 + " : " + dataset2[i].score2 * 100 +"%" +'\n' + dataset2[i].candidat3 + " : " + dataset2[i].score3 * 100 +"%"+ '\n';})
	};
};
