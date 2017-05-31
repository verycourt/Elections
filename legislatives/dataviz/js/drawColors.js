var svg = d3.select("svg")
var dataset = []

d3.csv('data/resultats.csv')
.row(function(d, i){
	return {
	circo : +d.circo,
	candidat1 : +d.candidat1,
	candidat2 : +d.candidat2,
	candidat3 : +d.candidat3,
	candidat4 : +d.candidat4
	};
})
.get(function(error, rows){
	dataset = rows;
	console.log("loaded : " + rows.length + " rows");
	draw();
	});

function draw(){
	svg
	.selectAll("path")
	.data(dataset)
	.enter()
	.select("title")
	.attr("Candidat1", "X")};
