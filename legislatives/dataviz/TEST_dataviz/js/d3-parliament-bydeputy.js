/*
 * MIT License
 * © Copyright 2016 - Geoffrey Brossard (me@geoffreybrossard.fr)
 */

var dicoNuances2 = {"EXG":"#d30202", "COM":"#990000", "FI":"#ff1616","SOC":"#f76060","RDG":"#edafaf",
"ECO":"#41992f","DIV":"#d3913b","REG":"#54422b","REM":"#ffbf00","MDM":"#ed9302","UDI":"#536cad","LR":"#3c589e",
"DVD":"#132553","DLF":"#7928b7","FN":"#03174a","EXD":"#000a23","DVG":"#c66b9a"}

var dicoNuancesPartis = {"EXG":"Extrême Gauche", "COM":"Parti Communiste", "FI":"France Insoumise","SOC":"Parti Socialiste","RDG":"Radicaux de Gauche",
"ECO":"Parti Ecologiste","DIV":"Divers","REG":"Régionalistes","REM":"La République en Marche","MDM":"MoDem","UDI":"Union des Démocrates et Indépendants","LR":"Les Républicains",
"DVD":"Divers Droite","DLF":"Debout la France","FN":"Front National","EXD":"Extrême Droite","DVG":"Divers gauche"}


d3.parliament = function() {
    /* params */
    var width = 500,
        height = 250,
        innerRadiusCoef = 0.4;

    /* animations */
    var enter = {
            "smallToBig": true,
            "fromCenter": true
        },
        exit = {
            "bigToSmall": true,
            "toCenter": true
        };

    /* events */
    // d3.dispatch is used to coordinate events in this case
    var parliamentDispatch = d3.dispatch("click", "dblclick", "mousedown", "mouseenter",
        "mouseleave", "mousemove", "mouseout", "mouseover", "mouseup", "touchcancel", "touchend",
        "touchmove", "touchstart");

    function parliament(data) {
        data.each(function(d) {
			
            var outerParliamentRadius = Math.min(width/2.5, height);
            var innerParliementRadius = outerParliamentRadius * innerRadiusCoef;

            /* init the svg */
            var svg = d3.select(this);
            svg.classed("d3-parliament", true);
            svg.attr("width", width);
            svg.attr("height", height);		 


            /***
             * compute number of seats and rows of the parliament */
            var nSeats = 0;
			//console.log(data);
            d.forEach(
                function(p) {
                    //console.log(p.Id, p.seats);
                    nSeats += (typeof p.seats === 'number') ? Math.floor(p.seats) : p.seats.length; 
                }
                );

            var nRows = 0;
            var maxSeatNumber = 0;
            var b = 0.5;
            (function() {
                var a = innerRadiusCoef / (1 - innerRadiusCoef);
                while (maxSeatNumber < nSeats) {
                    nRows++;
                    b += a;
                    /* NOTE: the number of seats available in each row depends on the total number
                    of rows and floor() is needed because a row can only contain entire seats. So,
                    it is not possible to increment the total number of seats adding a row. */
                    maxSeatNumber = series(function(i) { return Math.floor(Math.PI * (b + i)); }, nRows-1);
                }
            })();


            /***
             * create the seats list */
            /* compute the cartesian and polar coordinates for each seat */
            var rowWidth = (outerParliamentRadius - innerParliementRadius) / nRows;
            var seats = [];
            (function() {
                var seatsToRemove = maxSeatNumber - nSeats;
                // loop over the 13 rows
                for (var i = 0; i < nRows; i++) {
                    var rowRadius = innerParliementRadius + rowWidth * (i + 0.5);
                    var rowSeats = Math.floor(Math.PI * (b + i)) - Math.floor(seatsToRemove / nRows) - (seatsToRemove % nRows > i ? 1 : 0);
                    var anglePerSeat = Math.PI / rowSeats;
                    // lover over "columns"
                    for (var j = 0; j < rowSeats; j++) {
                        var s = {};
                        //console.log(i, j)
                        // rowRadius >>> 1 par parti élu
                        //s.deputy = d.party.deputies[j]
                        s.polar = {
                            r: rowRadius,
                            teta: -Math.PI + anglePerSeat * (j + 0.5)
                        };
                        s.cartesian = {
                            x: s.polar.r * Math.cos(s.polar.teta),
                            y: s.polar.r * Math.sin(s.polar.teta)
                        };
                        seats.push(s);
                    }
                };
            })();

            /* sort the seats by angle */
            seats.sort(function(a,b) {
                return a.polar.teta - b.polar.teta || b.polar.r - a.polar.r;
            });

            /* fill the seat objects with data of its party and of itself if existing */
            (function() {
                var partyIndex = 0;
                var seatIndex = 0;
                seats.forEach(function(s) {
                    //console.log(s);
                    /* get current party and go to the next one if it has all its seats filled */
                    var party = d[partyIndex];
                    var nSeatsInParty = typeof party.seats === 'number' ? party.seats : party.seats.length;
                    if (seatIndex >= nSeatsInParty) {
                        partyIndex++;
                        seatIndex = 0;
                        party = d[partyIndex];
                    }

                    /* set party data */
                    s.party = party;
                    s.data = typeof party.seats === 'number' ? null : party.seats[seatIndex];

                    seatIndex++;
                });
            })();


            /***
             * helpers to get value from seat data */
            var seatClasses = function(d) {
                var c = "seat ";
                c += (d.party && d.party.Id) || "";
                return c.trim();
            };
            var seatX = function(d) { return d.cartesian.x; };
            var seatY = function(d) { return d.cartesian.y; };
            var seatID = function(d) {
                return d.data.Désignation
                //return (Math.round(d.cartesian.x * 100) / 100).toString() + "__" + (Math.round(d.cartesian.y * 100) / 100).toString();
            };
            var seatRadius = function(d) {
                var r = 0.4 * rowWidth;
                if (d.data && typeof d.data.size === 'number') {
                    r *= d.data.size;
                }
                return r;
            };


            /***
             * fill svg with seats as circles */
            /* container of the parliament */
            var container = svg.select(".parliament");
            if (container.empty()) {
                container = svg.append("g");
                //console.log(d)
                container.classed("parliament", true);
            }
            container.attr("transform", "translate(" + (width) / 2 + "," + outerParliamentRadius + ")");
			
			
			  
            /* all the seats as circles */
            var circles = container.selectAll(".seat").data(seats);
            circles.attr("class", seatClasses);


            /* animation adding seats to the parliament */
            var circlesEnter = circles.enter().append("circle");
            circlesEnter.attr("class", seatClasses);
            circlesEnter.attr("cx", enter.fromCenter ? 0 : seatX);
            circlesEnter.attr("cy", enter.fromCenter ? 0 : seatY);
            circlesEnter.attr("r", enter.smallToBig ? 0 : seatRadius);
            circlesEnter.attr("id", seatID);
            if (enter.fromCenter || enter.smallToBig) {
                var t = circlesEnter.transition().duration(function() { return 1000 + Math.random()*80; });
                if (enter.fromCenter) {
                    t.attr("cx", seatX);
                    t.attr("cy", seatY);
                }
                if (enter.smallToBig) {
                    t.attr("r", seatRadius);
                }
            }


            // INIT ######################################################################################################

                        // histogram of the party
            /*d3.select("#img-histo").selectAll("img").remove(); 
            d3.select("#img-histo")
                .append('img')
                .attr("id", "my_histo")
                .attr("height", 150)
                .attr("src", "img/histo_REM.png");*/

            // toggle button
            /*d3.select("#img-histo").selectAll("input").remove(); 
            d3.select("#img-histo")
                .append("input")
                .attr("type", 'checkbox')
                .attr("checked", "checked")
                .attr("data-toggle", 'toggle');*/
                //data-toggle='toggle' data-on='Age' data-off='Sexe' data-onstyle='success' data-offstyle='danger' type='checkbox'");

           // remove selectedParty class
           // console.log(d3.selectAll(".seat")._groups[0])
           /*d3.selectAll(".seat")._groups[0].forEach(
               function(p) {
                   //console.log(pol);
                   d3.selectAll(".REM")
                       .attr("class", "seat REM");
            });

           // add this class to the selection
           d3.selectAll(".REM")
               .attr("class", "seat REM" + " selectParty");
                
            //console.log("img/carte_"+d.party.Id+".PNG")
            
            d3.select("#img-box").selectAll("img").remove();
            d3.select("#img-box")
              .append('img')
              .attr("src", "img/carte_REM"+".PNG")
              .attr("height", 330)
              .attr("x", 0)
              .attr("y", 0);*/


            /* circles catch mouse and touch events */
            for (var evt in parliamentDispatch._) {
                (function(evt){

                    //console.log('container.selectAll("input")', container.selectAll("input"));
                    /*container.selectAll("input").enter().on("click", function(r){

                        var bt_ = r.getAttribute("class").split(" ")[-1];
                        console.log("VOICI MA VARIABLE", bt_);
                    });*/
                    
                    circlesEnter.on(evt, function(e) { 
                        //console.log("e", e)
                        parliamentDispatch.call(evt, this, e);
                    });


                    /*$('.row .btn').on('click', function(e) {
                        console.log("moot2!");
                    });*/
                    //var r = d3.select(".toggle");
                    //r.onclick  = function() { alert("moot!"); };
                    //r.enter().on("click", function(s){alert("moot2!");});

                    circlesEnter
                        .on("click", function(d){

                            // show toogle button
                            d3.select("#img-histo").attr("class", "col-md-5");


                            // histogram of the party
                            d3.select("#img-histo").selectAll("img").remove(); 
                            d3.select("#img-histo")
                                .append('img')
                                .attr("class", "histo")
                                .attr("height", 150)
                                .attr("src", "js/screenshots_histogrammes/age_" + d.party.Id +".png");
                                //.attr("src", "img/histo_REM.png");

                            // toggle button
                            /*d3.select("#img-histo").selectAll("input").remove(); 
                            d3.select("#img-histo")
                                .append("input")
                                .attr("type", 'checkbox')
                                .attr("checked", "checked")
                                .attr("data-toggle", 'toggle');*/
                                //data-toggle='toggle' data-on='Age' data-off='Sexe' data-onstyle='success' data-offstyle='danger' type='checkbox'");

                           // remove selectedParty class
                           // console.log(d3.selectAll(".seat")._groups[0])
                           d3.selectAll(".seat")._groups[0].forEach(
                               function(p) {
                                   //console.log(p);
                                   var pol = p.getAttribute("class").split(" ")[1];
                                   //console.log(pol);
                                   d3.selectAll("." + pol)
                                       .attr("class", "seat " + pol);
                            });

                           // add this class to the selection
                           d3.selectAll("." + d.party.Id)
                               .attr("class", "seat " + d.party.Id + " selectParty");
                                
                            //console.log("img/carte_"+d.party.Id+".PNG")
                            
                              d3.select("#img-box").selectAll("img").remove();
                              d3.select("#img-box")
                              .append('img')
                              .attr("src", "img/carte_"+d.party.Id+".PNG")
                              .attr("height", 330)
                              .attr("x", 0)
                              .attr("y", 0);
                            
                        })
                        .on("mouseover", function(d){


                            // add the DEPUTY PICTURE


                              //console.log(d.data.link_vignes_x);
                              
                              d3.select("#imgtete").selectAll("img").remove();
                              d3.select("#imgtete")
                              .append('img')
                              .attr("src", d.data.link_vignes_x)
                              .attr("class", "img-rounded");


                            // add the MODEL INFORMATIONS about the deputy

                            if (d.party.membre_majorite == 0) {
                                maj = "<strong>Non</strong> ";
                            } else {
                                maj = "<strong>Oui</strong> ";
                            }
                            if (d.data.ancien_ministre == 0) {
                                ministre = "<strong>Non</strong>   <span style='visibility: hidden;'>.</span>";
                            } else {
                                ministre = "<strong>Oui</strong>   <span style='visibility: hidden;'>.</span>";
                            }
                            
                            if (d.data.pred_elu == "N") {
                                pred_elu = "<strong style='color:red'>Non</strong> ";
                            } else {
                                pred_elu = "<strong style='color:green'>Oui</strong> ";
                            }

                            if (d.data.depute_sortant == 0) {
                                sortant_ = "<strong>Non</strong> ";
                            } else {
                                sortant_ = "<strong>Oui</strong> ";
                            }

                            if (d.data.pred_elu == "N") {
                                color_pred = "red";
                            } else {
                                color_pred = "green";
                            }

                            
                            
                            d3.select(".baseline")
                              .html("<h3> Dans la circonscription "+ d.data.code.split("|")[1]+" du département "+ d.data.corr_dept + "</h3> "
                               +"<h4> Circonscription gagnée par : "+dicoNuancesPartis[d.party.Id]+"</h4> "
                               +"<table style='font-size:13px;'>"
                               +"<tr>"
                               +"<td>&#x2022; Score du parti aux présidentielles dans la circ. : <strong>"+ Math.round(d.data.score_bloc_pres*10000)/100+"%  <span style='opacity:0;'>.</span></strong> </td>"
                                +"<td>&#x2022; Part des ménages imposés dans la circ. : <strong>"+ Math.round(d.data.part_impose*10000)/100+"% </strong> </td>"
                               +"</tr>"
                                
                               +"<tr>"
                               +"<td>&#x2022; Chômage dans le département : <strong>"+Math.round(d.data.chom_tot*10000)/100+"%</strong> </td>"
                               +"<td>&#x2022; Revenu mensuel médian dans la circ. : <strong>"+d.data.revenus_med+"€</strong> </td>"
                               +"</tr>"
                                
                                +"<tr>"
                                +"<td>&#x2022; Part d'étrangers dans la circ. :  <strong>"+Math.round(d.data.etrangers*10000)/100+"%</strong> </td>"
                                +"<td>&#x2022; Nombre d'inscrits dans la circ. <strong>"+d.data.inscrits+"</strong> </td>"
                               +"</tr>"
                               +"</table>"
               
                               );
                            //console.log($(this));
                            //$(this).wrap("<a class='minitooltip' href='#' data-toggle='my_tooltip' data-placement='bottom' title='Hooray!' />");
                            //console.log(d.data)
                            d3.select(".col-md-7")
                                .append("div")
                                .attr('class','my_tooltip')
                                .style("background",'#F2EDED')
                                .style("border-color",color_pred)
                                .style("position", "absolute")
                                .style("z-index", "10 !important")
                                .html("<span style='font-size:120%;'>" + d.data.Désignation + "</span><br>"
                                    //+ "Département : " + d.data.Dpt + "<br>"
                                    + "Prédiction correcte ? <strong>" + pred_elu + "</strong><br>"
                                    + "Score 2nd tour : <strong>" + d.data.Score + "</strong><br>"
                                    + "Score 1er tour : <strong>" + d.data.score_exp + " %</strong><br>"
                                    + "Député sortant ? " + sortant_ + "<br>"
                                    //+ "Si ex-poste important : " + d.data["Perso."] + "<br>"
                                    + "Age : <strong>" + d.data.age + "</strong><br>"
                                    + "Profession : <strong>" + d.data.Profession.substring(4) + "</strong>"
                                    );
                                /*.html("<a href='#' data-toggle='my_tooltip' data-placement='bottom' title='Hooray!'>Bottom</a>")*/


                            /*console.log(this);
                            this.style("stroke-width", 3)
                                .style("stroke", color_pred);*/

                        })
                        .on("mousemove", function(){
                            d3.select(".my_tooltip").style("top", (d3.event.pageY-270)+"px").style("left",(d3.event.pageX+10)+"px");
                        })
                        .on("mouseout", 
                            function(){
                                //d3.select(".baseline").remove();
                                d3.select(".my_tooltip").remove();
                        });
                })(evt);
            }

            /* animation updating seats in the parliament */
            circles.transition().duration(function() { return 1000 + Math.random()*80; })
                .attr("cx", seatX)
                .attr("cy", seatY)
                .attr("r", seatRadius);

            /* animation removing seats from the parliament */
            if (exit.toCenter || exit.bigToSmall) {
                var t = circles.exit().transition().duration(function() { return 1000 + Math.random()*80; });
                if (exit.toCenter) {
                    t.attr("cx", 0).attr("cy", 0);
                }
                if (exit.bigToSmall) {
                    t.attr("r", 0);
                }
                t.remove();
            } else {
                circles.exit().remove();
            }
        });
    }

    parliament.width = function(value) {
        if (!arguments.length) return width;
        width = value;
        return parliament;
    };

    parliament.height = function(value) {
        if (!arguments.length) return height;
        height = value;
        return parliament;
    };

    parliament.innerRadiusCoef = function(value) {
        if (!arguments.length) return innerRadiusCoef;
        innerRadiusCoef = value;
        return parliament;
    };

    parliament.enter = {
        smallToBig: function (value) {
            if (!arguments.length) return enter.smallToBig;
            enter.smallToBig = value;
            return parliament.enter;
        },
        fromCenter: function (value) {
            if (!arguments.length) return enter.fromCenter;
            enter.fromCenter = value;
            return parliament.enter;
        }
    };

    parliament.exit = {
        bigToSmall: function (value) {
            if (!arguments.length) return exit.bigToSmall;
            exit.bigToSmall = value;
            return parliament.exit;
        },
        toCenter: function (value) {
            if (!arguments.length) return exit.toCenter;
            exit.toCenter = value;
            return parliament.exit;
        }
    };

    parliament.on = function(type, callback) {
        parliamentDispatch.on(type, callback);
    }

    return parliament;

    // util
    function series(s, n) { var r = 0; for (var i = 0; i <= n; i++) { r+=s(i); } return r; }

}
