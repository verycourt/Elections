var svg = d3.select("#premier")
var dataset = []
var dicoNuances = {"EXG":"#d30202", "COM":"#ff1616", "FI":"#ff1616","SOC":"#f76060","RDG":"#edafaf",
"ECO":"#41992f","DIV":"#d3913b","REG":"#54422b","REM":"#af4608","MDM":"#ea681c","UDI":"#b3c5f2","LR":"#3c589e",
"DVD":"#1a3372","DLF":"#0f2763","FN":"#03194f","EXD":"#000a23",'DVG':'#c66b9a'}


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

function color(){
	console.log(dataset.length);
	for(i=0;i < dataset.length; i++){
		console.log(dataset[i]);
		svg.select('[id='+'"'+dataset[i].circo+'"'+']')
		.style("fill", dicoNuances[dataset[i].color1])
		.select("title").text(function(){
		
		if(+dataset[i].score1 > 0.5){
			return dataset[i].nom +'\n' + dataset[i].candidat1 + ' ' +dataset[i].color1 + " : " + Math.round(dataset[i].score1 * 100) +"%" + "(Vainqueur au premier tour)";}
		
		else{
			if(+dataset[i].score1 > 0.5){
			return dataset[i].nom +'\n' + dataset[i].candidat1 + ' '+dataset[i].color1 + " : " + Math.round(dataset[i].score1 * 100) +"%" + "(Vainqueur au premier tour)";}
			
			else{
				if (+dataset[i].candidat3 == ''){
					return dataset[i].nom +'\n' + dataset[i].candidat1 + dataset[i].color1 +  " : " + Math.round(dataset[i].score1 * 100) +"%"  + '\n' 
					+ dataset[i].candidat2 + dataset[i].color2 + " : " + Math.round(dataset[i].score2 * 100) +"%";}
				
				else{
				if (+dataset[i].candidat4 == ''){
					return dataset[i].nom +'\n' + dataset[i].candidat1 + dataset[i].color1 +  " : " + Math.round(dataset[i].score1 * 100) +"%"  + '\n' 
					+ dataset[i].candidat2 +' '+ dataset[i].color2 + " : " + Math.round(dataset[i].score2 * 100) +"%" +'\n' + dataset[i].candidat3 + ' '+ dataset[i].color3 + " : " + Math.round(dataset[i].score3 * 100) +"%"+ '\n';}
					
				else{
					return dataset[i].nom +'\n' + dataset[i].candidat1 + ' ' + dataset[i].color1 +  " : " + Math.round(dataset[i].score1 * 100) +"%"  + '\n' 
					+ dataset[i].candidat2 + ' '+ dataset[i].color2 + " : " + Math.round(dataset[i].score2 * 100) +"%" +'\n' + dataset[i].candidat3 + ' ' + dataset[i].color3 + " : " + Math.round(dataset[i].score3 * 100) +"%"+ '\n'
					+ dataset[i].candidat4 + ' ' + dataset[i].color4 + " : " + Math.round(dataset[i].score4 * 100) +"%";}
					}
				}
			}
		})
	};};
