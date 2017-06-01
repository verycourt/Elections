var svg = d3.select("#svg4195")
var dataset = []

d3.csv('data/resultats.csv')
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
	dataset = rows;
	color();
	});

function color(){
	console.log("Drawing");
	for(i=0;i < dataset.length; i++){
		console.log(dataset[i]);
		svg.select('[id='+'"'+dataset[i].circo+'"'+']')
		.style("fill", dataset[i].color1)
		.select("title").text(dataset[i].nom +'\n' + dataset[i].candidat1 + " : " + dataset[i].score1 +'\n' 
		+ dataset[i].candidat2 + " : " + dataset[i].score2 +'\n' + dataset[i].candidat3 + " : " + dataset[i].score3 + '\n');
	};
};
