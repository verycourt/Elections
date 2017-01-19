
// inspirations: http://stackoverflow.com/questions/18790941/updating-the-data-of-a-pack-layout-from-json-call-and-redrawing
// inspirations: http://jsfiddle.net/nrndh3cn/
// inspirations: http://bl.ocks.org/alansmithy/e984477a741bc56db5a5

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

var svghist = d3.select("body").append("svg")
    .attr("width", widthhist + marginhist.left + marginhist.right)
    .attr("height", heighthist + marginhist.top + marginhist.bottom)
  .append("g")
    .attr("transform", "translate(" + marginhist.left + "," + marginhist.top + ")");

var currentJson;
var currentUrl = "j-4.json";

var getNewData = function() {

	//var day = $('input[name=day]:checked').val();

	dayStr = currentUrl.replace('j-', '').replace('.json', '');
	dayInt = parseInt(dayStr);

    if( dayInt > 1 ) {
    	nextDayInt = dayInt - 1;
        currentUrl = "j-" + nextDayInt.toString() + ".json";
    }

    console.log(currentUrl)

    //currentUrl = day + ".json";

    /*d3.json(currentUrl, function(error, data) {
        currentJson = data;
        refresh();
    });*/

    d3.json(currentUrl, function(error, root) {
      if (error) throw error;

      currentJson = root;
      refresh();

      /*partitionhist.nodes(root);
      xhist.domain([0, root.value]).nice();
      down(root, 0);*/
    });
}

var refresh = function () {

  //svghist = svg.select("g").data(currentJson);

  svghist.append("text")
    .attr("y", -40)
    .attr("x", 369)
    .style("text-anchor", "middle")
    .style("font-weight","bold")
    .style("font-size","25px")
    .style("fill", "#000000")
    .text("Mentions twitter par candidats sur une journée");


  svghist.append("rect")
      .attr("class", "background")
      .attr("id","backmentions")
      .attr("width", widthhist)
      .attr("height", heighthist)
      //.on("click", up);

  svghist.append("g")
      .attr("class", "x axis");

  svghist.append("g")
      .attr("class", "y axis")
    .append("line")
      .attr("y1", "100%");

  partitionhist.nodes(currentJson);
  xhist.domain([0, currentJson.value]).nice();
  down(currentJson, 0);

  //console.log('currentJson', currentJson)

}

  // LOADING MULTIPLE JSON FILES    WIPPPPPPPPP

  /*

  // we need a function to load files
  // done is a "callback" function
  // so you call it once you're finished and pass whatever you want
  // in this case, we're passing the `responseText` of the XML request
  var loadFile = function (filePath, done) {
      var xhr = new XMLHTTPRequest();
      xhr.onload = function () { return done(this.responseText) }
      xhr.open("GET", filePath, true);
      xhr.send();
  }
  // paths to all of your files
  var myFiles = [];
  for (numTweets=1; numTweets < 19; numTweets++) {
  	myFiles.push("j-" + numTweets.toString() + ".json")
  }

  // where you want to store the data
  var jsonData = [];
  // loop through each file
  myFiles.forEach(function (file, i) {
      // and call loadFile
      // note how a function is passed as the second parameter
      // that's the callback function
      loadFile(file, function (responseText) {
          // we set jsonData[i] to the parse data since the requests
          // will not necessarily come in order
          // so we can't use JSONdata.push(JSON.parse(responseText));
          // if the order doesn't matter, you can use push
          jsonData[i] = JSON.parse(responseText);
          // or you could choose not to store it in an array.
          // whatever you decide to do with it, it is available as
          // responseText within this scope (unparsed!)
          console.log(jsonData[i])
      })
  })

  */

  /*d3.json(currentUrl, function(error, root) {
    if (error) throw error;

    partitionhist.nodes(root);
    xhist.domain([0, root.value]).nice();
    down(root, 0);
  });*/

function down(d, i) {

  if (!d.children || this.__transition__) return;
  var end = durationhist + d.children.length * delay;

  // Mark any currently-displayed bars as exiting.
  var exit = svghist.selectAll(".enter")
      .attr("class", "exit");

  // Entering nodes immediately obscure the clicked-on bar, so hide it.
  /*exit.selectAll("rect").filter(function(p) { return p === d; })
      .style("fill-opacity", 1e-6);*/

	//console.log('d.children[0]', d.children[0])

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
      .style("cursor", function(d) { return !d.children ? null : "pointer"; })
      .on("click", down)
      .on("click", getNewData);

  bar.append("text")
      .attr("x", -6)
      .attr("y", barhistHeight / 2)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d.name; });

  //console.log('d.name', d.name)

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

document.getElementById("add_day")
	.addEventListener("click", getNewData);
//document.getElementById("form").addEventListener("click", getNewData);

d3.select(self.frameElement).style("height", "300px");

getNewData();