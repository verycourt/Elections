
var marginhist = {top: 60, right: 120, bottom: 0, left: 80},
    widthhist = 1000 - marginhist.left - marginhist.right,
    heighthist = 370 - marginhist.top - marginhist.bottom;

var xhist = d3.scale.linear()
    .range([0, widthhist]);

var barhistHeight = 20;

var colorhist = d3.scale.ordinal()
    .range(["#1DA1F2", "#1DA1F2"]);

var durationhist = 750,
    delay = 25;

var partitionhist = d3.layout.partition()
    .value(function(d) { return d.size; });

var xAxishist = d3.svg.axis()
    .scale(xhist)
    .orient("top");

var svghist = d3.select("#histogram").append("svg")
    .attr("width", widthhist + marginhist.left + marginhist.right)
    .attr("height", heighthist + marginhist.top + marginhist.bottom)
  .append("g")
    .attr("transform", "translate(" + marginhist.left + "," + marginhist.top + ")");

var currentJson;
var currentUrl = "j-1.json";

var daymax = 18;
var day = 'yesterday';
var nextDayInt = 1;

var initialize = function() {


  svghist.append("rect")
    .attr("class", "background")
    .attr("id","backmentions")
    .attr("width", widthhist)
    .attr("height", heighthist);

  svghist.append("g")
      .attr("class", "x axis");

  svghist.append("g")
      .attr("class", "y axis")
    .append("line")
      .attr("y1", "100%");

}

var getNewData = function(day) {

	dayCurrStr = currentUrl.replace('j-', '').replace('.json', '');
	dayCurrInt = parseInt(dayCurrStr);


	if ( day == "dayAfter" && dayCurrInt > 1 ) {

		nextDayInt = dayCurrInt - 1;
		currentUrl = "j-" + nextDayInt.toString() + ".json";

	} else if ( day == "dayBefore" && dayCurrInt < daymax ) {

		nextDayInt = dayCurrInt + 1;
		currentUrl = "j-" + nextDayInt.toString() + ".json";

	} else if ( day == "yesterday" ) {

		currentUrl = "j-1.json";
		nextDayInt = 1;
	}

	console.log('currentUrl', currentUrl);

  var d = new Date();
  d.setDate(d.getDate() - nextDayInt - 1);
  var dd = d.getDate();
  var mm = d.getMonth()+1; //January is 0!
  var yyyy = d.getFullYear();
  dayConsidered = dd+'/'+mm+'/'+yyyy;

  textTitle = "Mentions Twitter par candidats sur la journée du " + dayConsidered;




	d3.json(currentUrl, function(error, root) {
	if (error) throw error;

	currentJson = root;
	refresh();

  });
}

var refresh = function () {


  partitionhist.nodes(currentJson);
  xhist.domain([0, currentJson.value]).nice();
  down(currentJson, 0);


}


function down(d, i) {

  if (!d.children || this.__transition__) return;
  var end = durationhist + d.children.length * delay;

  // Mark any currently-displayed bars as exiting.
  var exit = svghist.selectAll(".enter")
      .attr("class", "exit");

  // Enter the new bars for the clicked-on data.
  // Per above, entering bars are immediately visible.
  var enter = bar(d)
      .attr("transform", stack(i))
      .style("opacity", 1);

  // Have the text fade-in, even though the bars are visible.
  // Color the bars as parents; they will fade to children if appropriate.
  enter.select("text").style("fill-opacity", 1e-6);
  enter.select("rect").style("fill", colorhist(true));

  // Update the x-scale domain.
  xhist.domain([0, d3.max(d.children, function(d) { return d.value; })]).nice();

  // Update the x-axis.
  svghist.selectAll(".x.axis").transition()
      .duration(durationhist)
      .call(xAxishist);

  // Transition entering bars to their new position.
  var enterTransition = enter.transition()
      .duration(durationhist)
      .delay(function(d, i) { return i * delay; })
      .attr("transform", function(d, i) { return "translate(0," + barhistHeight * i * 1.2 + ")"; });

  // Transition entering text.
  enterTransition.select("text")
      .style("fill-opacity", 1);

  //console.log('currentJson in down', currentJson)

  // Transition entering rects to the new x-scale.
  enterTransition.select("rect")
      .attr("width", function(d) { return xhist(d.value); })
      .style("fill", function(d) { return colorhist(!!d.children); });

  // Transition exiting bars to fade out.
  var exitTransition = exit.transition()
      .duration(durationhist)
      .style("opacity", 1e-6)
      .remove();

  // Transition exiting bars to the new x-scale.
  exitTransition.selectAll("rect")
      .attr("width", function(d) { return xhist(d.value); });

  svghist.append("text")
  .attr("class", "enter")
  .attr("y", -40)
  .attr("x", 369)
  .style("text-anchor", "middle")
  .style("font-weight","bold")
  .style("font-size","25px")
  .style("fill", "#000000")
  .text(textTitle);

  // Rebind the current node to the background.
  svghist.select(".background")
      .datum(d)
    .transition()
      .duration(end);

  d.index = i;
}

// Creates a set of bars for the given data node, at the specified index.
function bar(d) {
  var bar = svghist.insert("g", ".y.axis")
      .attr("class", "enter")
      .attr("transform", "translate(0,5)")
    .selectAll("g")
      .data(d.children)
    .enter().append("g")
      .style("cursor", function(d) { return !d.children ? null : "pointer"; });

  bar.append("text")
      .attr("x", -6)
      .attr("y", barhistHeight / 2)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d.name; });


  bar.append("rect")
      .attr("width", function(d) { return xhist(d.value); })
      .attr("height", barhistHeight);

	bar.append("text")
	  .attr("x", function(d) { return xhist(d.value); })
	  .attr("y", barhistHeight / 2)
	  .attr("dy", ".35em")
	  .style("font-weight", "bold")
	  .style("color", "red")
	  .text(function(d) { return d.value; });

  return bar;
}

// A stateful closure for stacking bars horizontally.
function stack(i) {
  var x0 = 0;
  return function(d) {
    var tx = "translate(" + x0 + "," + barhistHeight * i * 1.2 + ")";
    x0 += xhist(d.value);
    return tx;
  };
}


d3.select(self.frameElement).style("height", "300px");

initialize();
getNewData('yesterday');
