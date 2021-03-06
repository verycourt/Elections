var marginhist = {top: 60, right: 120, bottom: 0, left: 80},
    widthhist = 1000 - marginhist.left - marginhist.right,
    heighthist = 370 - marginhist.top - marginhist.bottom;

var colorhist = d3.scale.ordinal()
     .domain(["Hamon","Macron","Bayrou","Fillon",
	"Melenchon","Valls","Le Pen"])
     .range(["#CC3399","#A9A9A9","#A9A9A9","#0000CC",
	  "#FF0000",  "#CC3399","#000066"]);

var xhist = d3.scale.linear()
    .range([0, widthhist]);

var barhistHeight = 20;

<<<<<<< HEAD
var colorhist = d3.scale.ordinal()
      .domain(["Arnaud Montebourg", "Benoît Hamon","Cécile Duflot", "Emmanuel Macron",
          "François Bayrou",  "François Fillon",  "François Hollande",  "Jacques Cheminade",
          "Jean-Luc Mélenchon", "Manuel Valls", "Marine Le Pen",  "Nathalie Arthaud",
          "Nicolas Dupont-Aignan",  "Nicolas Hulot",  "Philippe Poutou",
          "Sylvia Pinel", "Yannick Jadot"])

      .range(["#CC0066", "#CC3399","#008000", "#A9A9A9",
          "#FF6600",  "#000080","#FF9999",  "#CC0000",
          "#FF0000",  "#FF6699",  "#3399FF",  "#CC0033",
          "#0000CC",  "#66CC00",  "#990033",
          "#FF0066",  "#339900"]);


=======
>>>>>>> 5095501b09af648a1595d1de9d9135cc65c9c521
var durationhist = 750,
    delay = 25;

var partitionhist = d3.layout.partition()
    .value(function(d) { return d.size; });

var xAxishist = d3.svg.axis()
    .scale(xhist)
    .orient("top");

var svghist = d3.select("#twittermentions").append("svg")
    .attr("width", "100%")
    .attr("height", "50%")
    .attr("viewBox","10 0 800 200")
    .append("g")
    .attr("transform", "translate(" + marginhist.left + "," + "5" + ")");


svghist.append("rect")
    .attr("class", "background")
    .attr("id","backmentions")
    .attr("width", widthhist)
    .attr("height", heighthist)
    .on("click", up);

svghist.append("g")
    .attr("class", "x axis");

svghist.append("g")
    .attr("class", "y axis")
  .append("line")
    .attr("y1", "100%");

d3.json("decompte/popcontest.json", function(error, root) {
  if (error) throw error;
  console.log(root);
  partitionhist.nodes(root);
  xhist.domain([0, root.value]).nice();
  down(root, 0);
});

function down(d, i) {
  if (!d.children || this.__transition__) return;
  var end = durationhist + d.children.length * delay;

  // Mark any currently-displayed bars as exiting.
  var exit = svghist.selectAll(".enter")
      .attr("class", "exit").style("font-size","1.5vmin");

  // Entering nodes immediately obscure the clicked-on bar, so hide it.
  exit.selectAll("rect").filter(function(p) { return p === d; })
      .style("fill-opacity", 1e-6);

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

  // Transition entering rects to the new x-scale.

  enterTransition.select("rect")
      .attr("width", function(d) { return xhist(d.value); })
      .style("fill", function(d) { return colorhist(d.name); });
<<<<<<< HEAD

=======
>>>>>>> 5095501b09af648a1595d1de9d9135cc65c9c521

  // Transition exiting bars to fade out.t
  var exitTransition = exit.transition()
      .duration(durationhist)
      .style("opacity", 1e-6)
      .remove();

  // Transition exiting bars to the new x-scale.
  exitTransition.selectAll("rect")
      .attr("width", function(d) { return x(d.value); });

  // Rebind the current node to the background.
  svghist.select(".background")
      .datum(d)
    .transition()
      .duration(end);

  d.index = i;
}

function up(d) {
  if (!d.parent || this.__transition__) return;
  var end = durationhist + d.children.length * delay;

  // Mark any currently-displayed bars as exiting.
  var exit = svghist.selectAll(".enter")
      .attr("class", "exit");

  // Enter the new bars for the clicked-on data's parent.
  var enter = bar(d.parent)
      .attr("transform", function(d, i) { return "translate(0," + barhistHeight * i * 1.2 + ")"; })
      .style("opacity", 1e-6);

  // Color the bars as appropriate.
  // Exiting nodes will obscure the parent bar, so hide it.
  enter.select("rect")
      .style("fill", function(d) { return colorhist(!!d.children); })
      .filter(function(p) { return p === d; })
      .style("fill-opacity", 1e-6);

  // Update the x-scale domain.
  x.domain([0, d3.max(d.parent.children, function(d) { return d.value; })]).nice();

  // Update the x-axis.
  svghist.selectAll(".x.axis").transition()
      .durationhist(durationhist)
      .call(xAxishist);

  // Transition entering bars to fade in over the full durationhist.
  var enterTransition = enter.transition()
      .durationhist(end)
      .style("opacity", 1);

  // Transition entering rects to the new x-scale.
  // When the entering parent rect is done, make it visible!
  enterTransition.select("rect")
      .attr("width", function(d) { return x(d.value); })
      .each("end", function(p) { if (p === d) d3.select(this).style("fill-opacity", null); });

  // Transition exiting bars to the parent's position.
  var exitTransition = exit.selectAll("g").transition()
      .durationhist(durationhist)
      .delay(function(d, i) { return i * delay; })
      .attr("transform", stack(d.index));

  // Transition exiting text to fade out.
  exitTransition.select("text")
      .style("fill-opacity", 1e-6);

  // Transition exiting rects to the new scale and fade to parent colorhist.
  exitTransition.select("rect")
      .attr("width", function(d) { return x(d.value); })
      .style("fill", colorhist(true));

  // Remove exiting nodes when the last child has finished transitioning.
  exit.transition()
      .durationhist(end)
      .remove();

  // Rebind the current parent to the background.
  svghist.select(".background")
      .datum(d.parent)
    .transition()
      .durationhist(end);
}

// Creates a set of bars for the given data node, at the specified index.
function bar(d) {
  var bar = svghist.insert("g", ".y.axis")
      .attr("class", "enter")
      .attr("transform", "translate(0,5)")
    .selectAll("g")
      .data(d.children)
    .enter().append("g")
      .style("cursor", function(d) { return !d.children ? null : "pointer"; })
      .on("click", down);

  bar.append("text")
      .attr("x", -6)
      .attr("y", barhistHeight / 3)
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
	  .style("font-size","2vmin")
	  .style("font-weight", "bold")
	  .style("text-anchor", "auto")
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
