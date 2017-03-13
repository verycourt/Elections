
function dashboard2(id, fData){
	
    function segColor(c){ return {
	"Emmanuel Macron":"#A9A9A9",
	"Jean-Luc Mélenchon" : "#FF0000",
	"Marine Le Pen":"#3399FF", 
	"François Fillon":"#000080",
	"Manuel Valls":"#FF6699",
	"Abstention, blanc ou nul":"#F5F5DC"}[c]; }
    
	var names = d3.keys(fData[0])
	
	var barColor = segColor(names[1]);
	
    // compute total for each state.
    fData.forEach(function(d){d.total=(d[names[1]]+d[names[2]]+d[names[3]])/100;});
    
    // function to handle histogram.
    function histoGram(fD){
        var hG={},    hGDim = {t: 60, r: 0, b: 20, l: 30};
        hGDim.w = 600 - hGDim.l - hGDim.r, 
        hGDim.h = 350 - hGDim.t - hGDim.b;
            
        //create svg for histogram.
        var hGsvg = d3.select(id).append("svg")
            .attr("width", "50%")
            .attr("height", "50%")
            .attr("viewBox","-25 -20 600 400","preserveAspectRatio", "xminYmin")
	    .append("g")
	    .attr("id","histo")	    
		// create function for x-axis mapping.
        var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.1)
                .domain(fD.map(function(d) { return d[0]; }));


        // Add x-axis to the histogram svg.
        hGsvg.append("g").attr("class", "x axis")
            .attr("transform", "translate(0," + hGDim.h + ")")
            .call(d3.svg.axis().scale(x)) 
	     .selectAll("text")
	     .style("text-anchor","end")
	     .attr("dx","-2em")
  	     //.attr("dy",".1em")
             .attr("transform",function(d) { return "rotate(-65)"})
	     .style("font-size","1vw");

        // Create function for y-axis map.
        var y = d3.scale.linear().range([hGDim.h, 0])
                .domain([0, d3.max(fD, function(d) { return d[1]; })]);

        // Create bars for histogram to contain rectangles and freq labels.
        var bars = hGsvg.selectAll(".bar").data(fD).enter()
                .append("g").attr("class", "bar");
				

		
        
        //create the rectangles.
        bars.append("rect")
            .attr("x", function(d) { return x(d[0]); })
            .attr("y", function(d) { return y(d[1]); })
            .attr("width", x.rangeBand())
            .attr("height", function(d) { return hGDim.h - y(d[1]); })
            .attr('fill',barColor)
      	    .style("stroke-linecap","round")
            .on("mouseover",mouseover)// mouseover is defined below.
            .on("mouseout",mouseout);// mouseout is defined below.
            
        //Create the frequency labels above the rectangles.
        bars.append("text").text(function(d){ return d3.format(",")(d[1])})
            .attr("x", function(d) { return x(d[0])+x.rangeBand()/2; })
            .attr("y", function(d) { return y(d[1])-5; })
            .attr("text-anchor", "middle");
        
		
		bars.append("text")
            .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
            .attr("transform", "translate("+ (hGDim.w/2) +","+(hGDim.h+(20))+")")  // centre below axis
            .style("font-family", "arial").text("Date du sondage");	
			
			
		bars.append("text")
            .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
            .attr("transform", "translate("+ (-10) +","+(hGDim.h/2)+")rotate(-90)")  // text is drawn off the screen top left, move down and out and rotate
            .style("font-size","1.1vw").style("font-family", "arial")
			.text("Intention de vote pour le candidat (en %)");
        function mouseover(d){  // utility function to be called on mouseover.
            // filter for selected state.
            var st = fData.filter(function(s){ return s.date == d[0];})[0],
                nD = names.slice(1,4).map(function(s){ return {type:s, freq:st[s]};});
               
            // call update functions of pie-chart and legend.    
            pC.update(nD);
            //leg.update(nD);
        }
        
        function mouseout(d){    // utility function to be called on mouseout.
            // reset the pie-chart and legend.    
            //pC.update(tF);
            //leg.update(tF);
        }
        
        // create function to update the bars. This will be used by pie-chart.
        hG.update = function(nD, color){
            // update the domain of the y-axis map to reflect change in frequencies.
            y.domain([0, d3.max(nD, function(d) { return d[1]; })]);
            
            // Attach the new data to the bars.
            var bars = hGsvg.selectAll(".bar").data(nD);
            
            // transition the height and color of rectangles.
            bars.select("rect").transition().duration(500)
                .attr("y", function(d) {return y(d[1]); })
                .attr("height", function(d) { return hGDim.h - y(d[1]); })
                .attr("fill", color);

            // transition the frequency labels location and change value.
            bars.select("text").transition().duration(500)
                .text(function(d){ return d3.format(",")(d[1])})
                .attr("y", function(d) {return y(d[1])-5; });            
        }        
        return hG;
    }
    
    // function to handle pieChart.
    function pieChart(pD){
        var pC ={},    pieDim ={w:250, h: 400};
        pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;
         
		var labelArc = d3.svg.arc()
		.outerRadius(pieDim.r - 20)
		.innerRadius(pieDim.r - 20);
	
        // create svg for pie chart.
        var piesvg = d3.select(id).append("svg")
        	.attr("width","45%").attr("height", "50%").attr("viewBox","-300 -350 600 600","preserveAspectRatio","xminYmin")
		.append("g")
	//.attr("transform", "translate("+"300"+","+"50"+")");
        // create function to draw the arcs of the pie slices.
        var arc = d3.svg.arc().outerRadius(pieDim.r - 10).innerRadius(0);

        // create a function to compute the pie slice angles.
        var pie = d3.layout.pie().sort(null).value(function(d) { return d.freq; });
		
		
		
        // Draw the pie slices.
        var svg = piesvg.selectAll("path").data(pie(pD)).enter()
		
		svg.append("path").attr("d", arc)
            .each(function(d) { this._current = d; })
            .style("fill", function(d) { return segColor(d.data.type); })
            .on("mouseover",mouseover).on("mouseout",mouseout)
			
		svg.append("svg:text").attr("transform",function(d) {
										d.innerRadius = 40;
										d.outerRadius = 40;
										var c  =arc.centroid(d);
										return "translate(" + c[0] + "," + c[1] + ")";									})
							.attr("text-anchor","middle")
							.style("font-size","0.8vw")
							.style("font-weight", "bold")
							.style("font-family", "sans-serif")
							.text(function(d) {return d.data.type;});
		
		svg.append("svg:text")
			.attr("text-anchor", "middle")// this makes it easy to centre the text as the transform is applied to the anchor
            .style("font-size","1.1vw")
			.attr("transform", "translate("+ (0) +","+(pieDim.r+10)+")")  // centre below axis
            .style("font-family", "sans-serif").text("Intentions de vote à la date sélectionnée");	
			

        // create function to update pie-chart. This will be used by histogram.
        pC.update = function(nD){
            piesvg.selectAll("path").data(pie(nD)).transition().duration(500)
                .attrTween("d", arcTween);
        }        
        // Utility function to be called on mouseover a pie slice.
        function mouseover(d){
            // call the update function of histogram with new data.
            hG.update(fData.map(function(v){
                return [v.date,v[d.data.type]];}),segColor(d.data.type));
        }
        //Utility function to be called on mouseout a pie slice.
        function mouseout(d){
            // call the update function of histogram with all data.
            //hG.update(fData.map(function(v){
              //  return [v.date,v[names[1]]];}), barColor);
        }
        // Animating the pie-slice requiring a custom function which specifies
        // how the intermediate paths should be drawn.
        function arcTween(a) {
            var i = d3.interpolate(this._current, a);
            this._current = i(0);
            return function(t) { return arc(i(t));    };
        }    
        return pC;
    }
    
    // function to handle legend.
    function legend(lD){
        var leg = {};
            
        // create table for legend.
        var legend = d3.select(id).append("table")
        .attr("transform", "translate(15%,-500)")
	.attr('class','legend');
        
        // create one row per segment.
   //     var tr = legend.append("tbody").selectAll("tr").data(lD).enter().append("tr");
            
		
        // create the first column for each segment.
        tr.append("td").append("svg").attr("width", '16').attr("height", '16').append("rect")
            .attr("width", '16').attr("height", '16')
			.attr("fill",function(d){ return segColor(d.type); })
			.on("mouseover",mouseover);
         
        // create the second column for each segment.
        //tr.append("td").text(function(d){ return d.type;});

        // create the fourth column for each segment.
        tr.append("td").attr("class",'legendPerc')
            .text(function(d){ return getLegend(d,lD);}).style("font-family", "sans-serif");

        // Utility function to be used to update the legend.
        leg.update = function(nD){
            // update the data attached to the row elements.
            var l = legend.select("tbody").selectAll("tr").data(nD);

            // update the frequencies.
            l.select(".legendFreq").text(function(d){ return d3.format(",")(d.freq);});

            // update the percentage column.
            l.select(".legendPerc").text(function(d){ return getLegend(d,nD);});        
        }
        
        function getLegend(d,aD){ // Utility function to compute percentage.
            return d3.format("%")(d.freq/d3.sum(aD.map(function(v){ return v.freq; })));
        }
		

		
		function mouseover(d){
            // call the update function of histogram with new data.
            hG.update(fData.map(function(v){
		
                return [v.date,v[d.type]];}),segColor(d.type));
				
        }

   //     return leg;
    }
    
    // calculate total frequency by segment for all state.
    var tF = [names[1],names[2],names[3]].map(function(d){ 
        return {type:d, freq: d3.sum(fData.map(function(t){ return t[d];}))}; 
    });    
    
    // calculate total frequency by state for all segment.
    var sF = fData.map(function(d){return [d.date,d[names[1]]];});

    var hG = histoGram(sF), // create the histogram.
        pC = pieChart(tF); // create the pie-chart.
        //leg= legend(tF);  // create the legend.
}


function afficher(nom){
		/*data.forEach(function(d) { // Make every date in the csv data a javascript date object format
		d.date = parseDate(d.date);
		});*/
		d3.tsv(nom, function(data) {
	  dashboard2('#dashboard',data);


	});
}
