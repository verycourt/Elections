var svg = d3.select("#premier")
var dataset = []
var dicoNuances = {"EXG":"#d30202", "COM":"#990000", "FI":"#ff1616","SOC":"#f76060","RDG":"#edafaf",
"ECO":"#41992f","DIV":"#d3913b","REG":"#54422b","REM":"#ffbf00","MDM":"#f4a213","UDI":"#537bbc","LR":"#3c589e",
"DVD":"#132553","DLF":"#7928b7","FN":"#03174a","EXD":"#000a23",'DVG':'#c66b9a'}


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
	score4 : d.score4,
	color2 : d.color2,
	color3 : d.color3,
	color4 : d.color4
	};
})
.get(function(error, rows){
	dataset = rows;
	color();
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
	//candidat4 : d.candidat4,
	//score4 : d.score4,
	color2 : d.color2,
	color3 : d.color3,
	//color4 : d.color4
	};
})
.get(function(error, rows){
	dataset = rows;
	color();
	});


function color(){
	console.log(dataset.length);
	for(i=0;i < dataset.length; i++){
		console.log(dataset[i]);
		var circo = svg.select('[id='+'"'+dataset[i].circo+'"'+']');
		circo
		.style("fill", dicoNuances[dataset[i].color1])
		.select("title").text(function(){
		
		if(+dataset[i].score1 > 0.5 && dataset[i].nom.indexOf('Français') < 0){
			circo.style("stroke","#000000").style("stroke-width","2");
			return dataset[i].nom +'\n' + dataset[i].candidat1 + ' ' +dataset[i].color1 + " : " + Math.round(dataset[i].score1 * 100) +"%" + " (Potentiel vainqueur au premier tour)"
			+ '\n' + dataset[i].candidat2 + ' ' +dataset[i].color2 + " : " + Math.round(dataset[i].score2 * 100) +"%"
			;}
		
			else{
				if (+dataset[i].candidat3 == ''){
					return dataset[i].nom +'\n' + dataset[i].candidat1 + ' '+ dataset[i].color1 +  " : " + Math.round(dataset[i].score1 * 100) +"%"  + '\n' 
					+ dataset[i].candidat2 + ' ' + dataset[i].color2 + " : " + Math.round(dataset[i].score2 * 100) +"%"
					;}
				
				else{
					circo.style("stroke","white").style("stroke-width","4");
					return dataset[i].nom +'\n' + dataset[i].candidat1 + ' ' +dataset[i].color1 +  " : " + Math.round(dataset[i].score1 * 100) +"%"  + '\n' 
					+ dataset[i].candidat2 +' '+ dataset[i].color2 + " : " + Math.round(dataset[i].score2 * 100) +"%" +'\n' + dataset[i].candidat3 + ' '+ dataset[i].color3 + " : " + Math.round(dataset[i].score3 * 100) +"%"+ '\n'
					;}
				/*if (+dataset[i].candidat4 == ''){
					circo.style("stroke","white").style("stroke-width","3");
					return dataset[i].nom +'\n' + dataset[i].candidat1 + ' ' +dataset[i].color1 +  " : " + Math.round(dataset[i].score1 * 100) +"%"  + '\n' 
					+ dataset[i].candidat2 +' '+ dataset[i].color2 + " : " + Math.round(dataset[i].score2 * 100) +"%" +'\n' + dataset[i].candidat3 + ' '+ dataset[i].color3 + " : " + Math.round(dataset[i].score3 * 100) +"%"+ '\n';}
					
				else{
					circo.style("stroke","black").style("stroke-width","3");
					return dataset[i].nom +'\n' + dataset[i].candidat1 + ' ' + dataset[i].color1 +  " : " + Math.round(dataset[i].score1 * 100) +"%"  + '\n' 
					+ dataset[i].candidat2 + ' '+ dataset[i].color2 + " : " + Math.round(dataset[i].score2 * 100) +"%" +'\n' + dataset[i].candidat3 + ' ' + dataset[i].color3 + " : " + Math.round(dataset[i].score3 * 100) +"%"+ '\n'
					+ dataset[i].candidat4 + ' ' + dataset[i].color4 + " : " + Math.round(dataset[i].score4 * 100) +"%";}*/
					}
				}
		)
	};
};
